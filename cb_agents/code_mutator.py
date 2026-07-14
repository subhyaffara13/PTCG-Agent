"""
cb_agents/code_mutator.py

Implements Self-Evolving Code Optimization (SECO).
Analyzes local match replays for passive play or crashes, generates code mutation prompts,
applies LLM-based refactoring (supporting Google Gemini, local Ollama, or file-based queueing),
runs unit test guardrails, and evaluates performance.
"""

import os
import sys
import json
import subprocess
import shutil
import logging
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger("code_mutator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

_PROJECT_ROOT = Path("C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent")
load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

_REPLAY_PATH = _PROJECT_ROOT / "visualizer" / "data" / "local_match_replay.json"
_LOG_PATH = _PROJECT_ROOT / "submission" / "logs" / "reasoning_log.json"
_EVOLUTION_LOG = _PROJECT_ROOT / "logs" / "evolution_log.json"

def analyze_recent_match_replay() -> dict:
    """Analyze the latest match replay to diagnose performance issues and bugs."""
    logger.info("Analyzing recent match replay for telemetry...")
    if not _REPLAY_PATH.exists():
        logger.warning(f"No replay file found at {_REPLAY_PATH}. Cannot collect telemetry.")
        return {"needs_fixing": False, "reason": "No replay found"}

    try:
        data = json.load(open(_REPLAY_PATH, encoding="utf-8"))
        steps = data.get("steps", [])
    except Exception as e:
        logger.error(f"Failed to parse replay file: {e}")
        return {"needs_fixing": False, "reason": f"Parse error: {e}"}

    total_steps = len(steps)
    attacks_count = 0
    passes_count = 0
    missed_attacks = 0
    total_decisions = 0
    crashed_steps = []

    # Read log entries to find exceptions or crashes
    has_crashes = False
    crash_details = []
    if _LOG_PATH.exists():
        try:
            entries = json.load(open(_LOG_PATH, encoding="utf-8"))
            for entry in entries:
                if "CRITICAL" in str(entry) or "Exception" in str(entry) or "Traceback" in str(entry):
                    has_crashes = True
                    crash_details.append(str(entry)[:300])
        except Exception:
            pass

    for step_idx, step in enumerate(steps):
        p1 = step[0] if step else {}
        obs = p1.get("observation", {}) if isinstance(p1, dict) else {}
        action = p1.get("action")
        status = p1.get("status")

        if status == "ERROR" or status == "TIMEOUT":
            crashed_steps.append(step_idx)

        select = obs.get("select", {}) if isinstance(obs, dict) else {}
        if not select:
            continue

        sel_type = select.get("type")
        sel_ctx = select.get("context")
        options = select.get("option", [])

        # Main turn decisions
        if sel_type == 0 and sel_ctx == 0:
            total_decisions += 1
            chosen_indices = action if isinstance(action, list) else ([action] if action is not None else [])
            
            has_attack_opt = False
            for opt in options:
                if isinstance(opt, dict) and opt.get("type") == 13:
                    has_attack_opt = True

            chose_pass = False
            chose_attack = False
            for idx in chosen_indices:
                if idx < len(options):
                    opt = options[idx]
                    if isinstance(opt, dict):
                        if opt.get("type") == 14:
                            chose_pass = True
                        elif opt.get("type") == 13:
                            chose_attack = True

            if chose_attack:
                attacks_count += 1
            if chose_pass:
                passes_count += 1
                if has_attack_opt:
                    missed_attacks += 1

    pass_ratio = passes_count / max(total_decisions, 1)
    needs_fixing = False
    issues = []

    if crashed_steps or has_crashes:
        needs_fixing = True
        issues.append(f"Crashes/Exceptions detected. Crashed steps: {crashed_steps}. Details: {crash_details[:3]}")
    if missed_attacks > 0 or pass_ratio > 0.25:
        needs_fixing = True
        issues.append(f"Passive play detected: missed {missed_attacks} attacks, pass ratio {pass_ratio:.1%}.")

    return {
        "needs_fixing": needs_fixing,
        "reason": "; ".join(issues) if issues else "Optimal play",
        "telemetry": {
            "total_steps": total_steps,
            "total_decisions": total_decisions,
            "attacks": attacks_count,
            "passes": passes_count,
            "missed_attacks": missed_attacks,
            "pass_ratio": pass_ratio,
            "has_crashes": has_crashes
        }
    }

def request_code_mutation_from_llm(file_path: Path, telemetry_issues: str) -> str:
    """Generate prompt and fetch code mutation from the best available LLM endpoint."""
    code_content = file_path.read_text(encoding="utf-8")
    
    prompt = f"""
    You are an expert AI code optimizer for a Pokémon TCG agent.
    The agent is playing suboptimally and we need to evolve its Python heuristics.
    
    CRITICAL ISSUES FOUND IN LOCAL SIMULATION:
    {telemetry_issues}
    
    Provide the complete, updated Python code that fixes these issues and improves the agent's logic.
    
    CRITICAL RESTRICTION: DO NOT delete any existing rules, helper functions, or core logic unless you are specifically rewriting them to be strictly better. Do not truncate the file. If you delete random code, the agent will crash and lose the game.
    
    - Leverage our MODULAR ARCHITECTURE: You can import and use helpers from:
      * `cb_agents.preference_maps` (fallback to `agents.preference_maps`): `get_energy_preference(card_id: str) -> str`
      * `cb_agents.lethal_detector` (fallback to `agents.lethal_detector`): `evaluate_active_danger(...) -> dict`
    - Keep code clean, modular, and extremely compact.
    - If the issue is PASSIVE PLAY, ensure attacks are heavily prioritized over passing when available.
    - If the issue is CRASHES or type errors (e.g. Struct/dict mismatches), add robust safe-extraction logic.
    - Keep all imports intact.
    - Do not change functions that are unrelated to the issues.
    
    CURRENT CODE OF {file_path.name}:
    ```python
    {code_content}
    ```
    
    INSTRUCTIONS:
    Analyze the issues and provide the complete, corrected python code. You must output a JSON object containing 'reasoning' (your step-by-step analysis) and 'mutated_code' (the updated code).
    """

    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if gemini_key:
        import requests
        models = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
        for model in models:
            try:
                logger.info(f"Connecting to Google Gemini API ({model}) for mutation...")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "responseMimeType": "application/json",
                        "responseSchema": {
                            "type": "OBJECT",
                            "properties": {
                                "reasoning": {
                                    "type": "STRING",
                                    "description": "Chain-of-thought analysis of the issues and the required code changes."
                                },
                                "mutated_code": {
                                    "type": "STRING",
                                    "description": "The complete, updated python code with all imports intact."
                                }
                            },
                            "required": ["reasoning", "mutated_code"]
                        }
                    }
                }
                res = requests.post(url, json=payload, headers=headers, timeout=60)
                if res.status_code == 200:
                    text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                    if text:
                        try:
                            data = json.loads(text)
                            code = data.get("mutated_code", "")
                            reason = data.get("reasoning", "")
                            logger.info(f"Mutation generated successfully using {model}. Reasoning:\n{reason}")
                            if code:
                                return code
                        except Exception as parse_e:
                            logger.warning(f"Failed to parse JSON response: {parse_e}. Falling back to clean_code_response on raw text...")
                            return clean_code_response(text)
                else:
                    logger.warning(f"Gemini API ({model}) returned status code {res.status_code}: {res.text}")
            except Exception as e:
                logger.warning(f"Gemini API ({model}) call failed: {e}")

    # 2. Try Local Ollama endpoint (Offline / Privacy-focused fallback)
    try:
        import requests
        logger.info("Attempting local Ollama API (localhost:11434) fallback...")
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "codellama:7b",
            "prompt": prompt,
            "stream": False
        }
        res = requests.post(url, json=payload, timeout=60)
        if res.status_code == 200:
            return clean_code_response(res.json().get("response", ""))
    except Exception as e:
        logger.warning(f"Local Ollama API unavailable: {e}")

    # 3. No LLM endpoint: log requests to logs/evolution_request.json for the Antigravity developer
    req_path = _PROJECT_ROOT / "logs" / "evolution_request.json"
    req_path.parent.mkdir(parents=True, exist_ok=True)
    request_data = {
        "file_to_mutate": str(file_path.relative_to(_PROJECT_ROOT)),
        "telemetry_issues": telemetry_issues,
        "prompt": prompt
    }
    req_path.write_text(json.dumps(request_data, indent=2), encoding="utf-8")
    logger.info(f"LLM endpoints unavailable. Mutation request queued to {req_path} for dev assistance.")
    return ""

def clean_code_response(text: str) -> str:
    """Strip markdown backticks from LLM responses to extract pure python."""
    text = text.strip()
    if text.startswith("```python"):
        text = text[9:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def run_evaluation_match() -> float:
    """Run validation match vs baseline and return the reward score."""
    logger.info("Running evaluation match for mutated code using the Gauntlet...")
    try:
        # Rebuild package first
        subprocess.run([sys.executable, "build_submission.py"], check=True, capture_output=True)
        
        from factory.gauntlet_runner import GauntletRunner
        from factory.game_runner import DEFAULT_DECK
        
        runner = GauntletRunner()
        # Run 2 games per gauntlet archetype
        win_rate = runner.run_gauntlet(DEFAULT_DECK, num_games_per_archetype=2)
        return float(win_rate)
    except Exception as e:
        logger.error(f"Evaluation match failed: {e}")
        return 0.0

def push_mutation_to_git(file_path: Path, issue_desc: str):
    """Automatically stage, commit, and push the verified mutation to git."""
    try:
        logger.info("Initiating automatic git commit and push for verified mutation...")
        # Stage changed files
        subprocess.run(["git", "add", str(file_path)], check=True)
        # Stage submission folder (build_submission.py will be run to regenerate main.py)
        subprocess.run([sys.executable, "build_submission.py"], check=True, capture_output=True)
        subprocess.run(["git", "add", "submission/"], check=True)
        
        # Commit message
        msg = f"Auto-evolve: Mutated {file_path.name} to fix: {issue_desc}"
        subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)
        
    except Exception as e:
        logger.error(f"Failed to auto-push mutation to git: {e}")

def run_evolution_cycle(target_file: str = "cb_agents/turn_planner_sort.py", telemetry: dict | None = None):
    """Orchestrates the entire code mutation and evolution cycle."""
    if telemetry is None:
        telemetry = analyze_recent_match_replay()
    if not telemetry.get("needs_fixing"):
        logger.info("Recent match telemetry shows optimal performance. Skipping evolution.")
        return

    file_path = _PROJECT_ROOT / target_file
    if not file_path.exists():
        logger.error(f"Target file {file_path} not found.")
        return

    import hashlib
    blacklist_path = _PROJECT_ROOT / "logs" / "blacklisted_mutations.json"
    blacklist = []
    if blacklist_path.exists():
        try:
            blacklist = json.loads(blacklist_path.read_text(encoding="utf-8"))
        except:
            pass

    feedback = telemetry["reason"]
    backup_path = file_path.with_suffix(".py.bak")
    shutil.copy2(file_path, backup_path)
    logger.info(f"Created backup of original file at {backup_path}")

    success = False
    for attempt in range(1, 4):
        logger.info(f"Evolution attempt {attempt}/3 for {target_file}...")
        mutated_code = request_code_mutation_from_llm(file_path, feedback)
        if not mutated_code:
            logger.error("Failed to fetch mutation from LLM.")
            break

        code_hash = hashlib.sha256(mutated_code.encode("utf-8")).hexdigest()
        if code_hash in blacklist:
            logger.warning(f"Generated mutation {code_hash} is blacklisted (failed previously). Retrying with penalty feedback...")
            feedback = "The code you just generated was already blacklisted because it failed unit tests. Try a completely different logic approach."
            continue

        try:
            # Apply mutation
            file_path.write_text(mutated_code, encoding="utf-8")
            logger.info(f"Applied mutation variant {code_hash}")

            # Guardrail 1: Run pytest
            logger.info("Running pytest guardrails...")
            test_res = subprocess.run(["pytest"], capture_output=True, text=True)
            if test_res.returncode != 0:
                raise Exception(f"Pytest suite failed: {test_res.stdout[-400:]}")
            logger.info("Pytest guardrails passed!")

            # Guardrail 2: Match evaluation
            score = run_evaluation_match()
            if score < 0.5:
                raise Exception(f"Evaluation win rate regressed: score={score}")
            logger.info("Evaluation match passed! Mutation promoted.")

            # Log successful evolution
            evolution_entry = {
                "timestamp": "now",
                "file": target_file,
                "issues_fixed": telemetry["reason"],
                "status": "PROMOTED",
                "hash": code_hash
            }
            logs = []
            if _EVOLUTION_LOG.exists():
                try:
                    logs = json.loads(_EVOLUTION_LOG.read_text(encoding="utf-8"))
                except:
                    pass
            logs.append(evolution_entry)
            _EVOLUTION_LOG.write_text(json.dumps(logs, indent=2), encoding="utf-8")

            # Clean up backup and commit
            backup_path.unlink()
            push_mutation_to_git(file_path, telemetry["reason"])
            success = True
            break

        except Exception as e:
            logger.warning(f"Attempt {attempt} failed: {e}. Blacklisting hash and retrying...")
            blacklist.append(code_hash)
            try:
                blacklist_path.write_text(json.dumps(blacklist, indent=2), encoding="utf-8")
            except:
                pass
            feedback = f"Your previous code modification failed with error: {str(e)}. Please fix this error and try a different logic."

    if not success:
        logger.error(f"All 3 evolution attempts failed. Restoring stable baseline from {backup_path}")
        shutil.move(backup_path, file_path)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "cb_agents/turn_planner_sort.py"
    run_evolution_cycle(target)
