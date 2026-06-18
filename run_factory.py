"""
run_factory.py

Main orchestrator script to execute a self-improving training loop iteration.
Ties together: GameRunner -> EvalAgent -> ImprovementAgent -> (BuilderAgent | DeckArchitect) -> ValidatorAgent.
"""

import sys
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("run_factory")

from factory.game_runner import GameRunner, DEFAULT_DECK
from factory.eval_agent import EvalAgent
from factory.improvement_agent import ImprovementAgent
from factory.builder_agent import BuilderAgent
from factory.deck_architect import DeckArchitect
from factory.validator_agent import ValidatorAgent

def run_iteration(iteration_id: int, forced_archetype: str = None, forced_change_type: str = None, forced_escalation: dict = None):
    logger.info(f"=== STARTING ITERATION {iteration_id} ===")

    # Initialize components
    runner = GameRunner()
    evaluator = EvalAgent()
    improver = ImprovementAgent()
    builder = BuilderAgent()
    architect = DeckArchitect()
    validator = ValidatorAgent()

    # Load baseline/current configurations
    skills_dir = Path("skills")
    priority_rules = {}
    if (skills_dir / "priority_rules.json").exists():
        try:
            priority_rules = json.loads((skills_dir / "priority_rules.json").read_text(encoding="utf-8"))
        except:
            pass

    strategy_profiles = {}
    if (skills_dir / "strategy_profiles.json").exists():
        try:
            strategy_profiles = json.loads((skills_dir / "strategy_profiles.json").read_text(encoding="utf-8"))
        except:
            pass

    # For base deck, use DEFAULT_DECK or custom list
    deck_base = DEFAULT_DECK
    deck_new = DEFAULT_DECK

    # STEP 1: Run simulation matches
    logger.info("Step 1: Running simulation matches...")
    version_n1 = f"base_v{iteration_id}"
    version_n2 = f"new_v{iteration_id}"

    iteration_result = runner.run_iteration(
        iteration_id=iteration_id,
        version_n1=version_n1,
        version_n2=version_n2,
        deck_base=deck_base,
        deck_new=deck_new,
        reasoning_base=priority_rules,
        reasoning_new=priority_rules
    )

    # STEP 2: Evaluate match outcomes
    logger.info("Step 2: Evaluating game results...")
    change_type = forced_change_type or "strategy_patch"
    archetype = forced_archetype or "aggro"
    
    eval_report = evaluator.evaluate(
        iteration_result=iteration_result,
        change_type=change_type,
        archetype=archetype
    )
    logger.info(f"Evaluation report generated. Best version: {eval_report['version_scores']['best_version']}")

    # STEP 3: Decide improvement policy
    logger.info("Step 3: Deciding improvement action...")
    improvement_notes = improver.improve(eval_report)
    if forced_escalation:
        logger.info(f"Overriding escalation policy with: {forced_escalation}")
        improvement_notes["escalation"].update(forced_escalation)
        if forced_escalation.get("builder_agent"):
            improvement_notes["action_taken"] = "escalate_builder_agent"
            improvement_notes["next_eval_context"] = "micro_patch"
        if forced_escalation.get("deck_architect"):
            improvement_notes["action_taken"] = "escalate_deck_architect"
            improvement_notes["next_eval_context"] = "deck_test"
    action_taken = improvement_notes["action_taken"]
    logger.info(f"Policy decision action: {action_taken}")

    # STEP 4: Build new logic or deck if escalated
    staged_file = None

    if improvement_notes["escalation"]["builder_agent"]:
        logger.info("Step 4a: Escalated to BuilderAgent. Generating code changes...")
        improvement_notes["iteration"] = iteration_id
        build_res = builder.build(improvement_notes)
        if build_res.get("status") == "success":
            staged_file = build_res.get("staging_path")
            logger.info(f"Staged modified logic file at: {staged_file}")

    if improvement_notes["escalation"]["deck_architect"]:
        logger.info("Step 4b: Escalated to DeckArchitect. Architecting deck configuration...")
        arch_res = architect.build(improvement_notes)
        if arch_res.get("status") == "success":
            staged_file = Path("staging") / "deck_new.csv"
            logger.info(f"Staged deck configuration at: {staged_file}")

    # STEP 5: Validate and promote changes
    if staged_file and Path(staged_file).exists():
        logger.info(f"Step 5: Running security and correctness validation on staged file: {staged_file}...")
        val_report = validator.validate(
            staged_file_path=str(staged_file),
            eval_report=eval_report
        )
        logger.info(f"Validation finished. Promoted live: {val_report.get('promoted', False)}")
        if val_report.get("promoted"):
            logger.info("Staged component has been successfully promoted to the live agents/skills folder!")
        else:
            logger.warning(f"Promotion failed. Reason: {val_report.get('reason')}")
    else:
        logger.info("No files staged for promotion in this iteration (e.g. weights tuned or build skipped).")

    # STEP 6: Save logs for Visualizer if marginal progress was shown
    try:
        best_ver = eval_report.get("version_scores", {}).get("best_version", "player_a")
        p_a_score = eval_report.get("version_scores", {}).get("player_a", 0.0)
        p_b_score = eval_report.get("version_scores", {}).get("player_b", 0.0)
        delta = p_b_score - p_a_score
        
        if best_ver == "player_b" and 0.0 < delta <= 0.35:
            logger.info(f"Iteration {iteration_id} showed marginal progress (delta: {delta:.4f}). Copying game steps to visualizer...")
            vis_dir = Path("visualizer") / "data"
            vis_dir.mkdir(parents=True, exist_ok=True)
            
            for label, game in iteration_result.get("games", {}).items():
                steps_filename = game.get("log_files", {}).get("steps")
                if steps_filename:
                    src_path = Path("logs") / steps_filename
                    if src_path.exists():
                        dest_path = vis_dir / f"iter_{iteration_id}_{label}.json"
                        dest_path.write_text(src_path.read_text(encoding="utf-8"), encoding="utf-8")
                        logger.info(f"Copied {steps_filename} -> {dest_path}")
    except Exception as e:
        logger.error(f"Error copying visualizer steps: {e}")

    logger.info(f"=== COMPLETED ITERATION {iteration_id} ===\n")

if __name__ == "__main__":
    start_iter = 1
    end_iter = 1
    if len(sys.argv) > 2:
        try:
            start_iter = int(sys.argv[1])
            end_iter = int(sys.argv[2])
        except ValueError:
            pass
    elif len(sys.argv) > 1:
        try:
            start_iter = int(sys.argv[1])
            end_iter = start_iter
        except ValueError:
            pass
            
    for iter_num in range(start_iter, end_iter + 1):
        run_iteration(iter_num)
