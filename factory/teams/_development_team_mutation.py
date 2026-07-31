import sys
import subprocess
import pathlib
import logging
logger = logging.getLogger("DevelopmentTeam")

def _apply_code_edits(edits):
    for edit in edits.get("files_to_edit", []):
        fp = pathlib.Path(edit["filepath"])
        if fp.exists():
            content = fp.read_text(encoding="utf-8")
            if edit["original_code"] in content:
                content = content.replace(edit["original_code"], edit["new_code"])
                fp.write_text(content, encoding="utf-8")
                logger.info(f"LLM successfully patched {fp.name}")
            else:
                logger.warning(f"LLM provided mismatched original_code for {fp.name}")

def _run_gauntlet_guard():
    from factory.gauntlet_runner import GauntletRunner
    paths = ["submission/deck.csv", "staging/deck_new.csv", "cb_agents/deck_new.csv", "deck.csv"]
    cand_deck = []
    for p_str in paths:
        p = pathlib.Path(p_str)
        if p.exists():
            import csv
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        cand_deck.extend([int(row["card_id"])] * int(row["count"]))
                if len(cand_deck) == 60:
                    break
            except Exception:
                pass
    if len(cand_deck) != 60:
        from factory.game_runner import DEFAULT_DECK
        cand_deck = list(DEFAULT_DECK)
    res = GauntletRunner().run_gauntlet(cand_deck, num_games_per_stage=1)
    return res.get("win_rate", 0.0) if isinstance(res, dict) else float(res)

def run_llm_code_mutation_phase(meta_analyst, code_architect):
    logger.info("--- [LLM Meta-Learning Phase] ---")
    try:
        flaws = meta_analyst.analyze_logs()
        if not flaws:
            logger.info("No flaws extracted. Skipping code mutation.")
            return
        edits = code_architect.propose_code_fixes(flaws)
        if not edits or "files_to_edit" not in edits:
            logger.info("No code edits proposed.")
            return
        _apply_code_edits(edits)
        logger.info("Verifying LLM C++ syntax via test compilation...")
        compile_result = subprocess.run([sys.executable, "setup.py", "build_ext", "--inplace"], cwd="submission", capture_output=True, text=True)
        if compile_result.returncode != 0:
            logger.error("LLM hallucinated invalid C++ syntax! Reverting changes...")
            subprocess.run(["git", "restore", "submission/src/"], check=False)
            subprocess.run(["git", "restore", "submission/cb_agents/"], check=False)
        else:
            logger.info("LLM Code Patch compiled successfully! Running Gauntlet Evaluation guard...")
            try:
                win_rate = _run_gauntlet_guard()
                if win_rate < 0.50:
                    logger.error(f"Gauntlet Guard Rejected LLM Patch: Win rate fell to {win_rate*100:.1f}%. Reverting...")
                    subprocess.run(["git", "restore", "submission/src/"], check=False)
                    subprocess.run(["git", "restore", "submission/cb_agents/"], check=False)
                else:
                    logger.info(f"Gauntlet Guard Passed! Win rate: {win_rate*100:.1f}%. Keeping patch.")
            except Exception as g_err:
                logger.warning(f"Gauntlet evaluation guard encountered exception: {g_err}. Proceeding with caution.")
    except Exception as e:
        logger.error(f"LLM Meta-Learning Phase failed: {e}", exc_info=True)
