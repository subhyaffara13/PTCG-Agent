import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

def determine_escalation(eval_report: dict) -> tuple:
    flags = eval_report.get("flags", {})
    flag_deck_architect = flags.get("flag_deck_architect", False)
    flag_builder_agent = flags.get("flag_builder_agent", False)
    
    if "meta_data" in eval_report or "macro_analysis" in eval_report:
        if eval_report.get("anti_patterns", {}).get("deck_donts"):
            flag_deck_architect = True
        if eval_report.get("anti_patterns", {}).get("behavior_donts"):
            flag_builder_agent = True
            
    recommendation = eval_report.get("recommendation", "status_quo")
    
    action = "tuned_weights"
    reasoning = "Normal operation. Tuning weights."
    if recommendation == "tune":
        action = "tuned_weights"
        reasoning = "Normal operation. Tuning evaluation weights."

    if flag_deck_architect and not flag_builder_agent:
        action = "escalate_deck_architect"
        reasoning = "Consecutive deck test failures detected. Escalated to Deck Architect."
    elif flag_builder_agent and not flag_deck_architect:
        action = "escalate_builder_agent"
        reasoning = "Consecutive logic test failures detected. Escalated to Builder Agent."
    elif flag_deck_architect and flag_builder_agent:
        action = "escalate_both"
        reasoning = "Consecutive failures detected in both deck and logic paths. Rebuilding both."

    if action == "escalate_deck_architect":
        next_context = "deck_test"
    elif action == "escalate_builder_agent":
        next_context = "micro_patch"
    elif action == "tuned_weights":
        next_context = eval_report.get("eval_context", "analytics_feedback")
    else:
        next_context = "meta_test"

    return action, reasoning, next_context

def append_decision(decisions_file: Path, iteration: int, action_taken: str, reasoning: str, next_eval_context: str, best_version: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n## Iteration {iteration} — {timestamp}\n"
        f"**Action:** {action_taken}\n"
        f"**Reasoning:** {reasoning}\n"
        f"**Next context:** {next_eval_context}\n"
        f"**Best version:** {best_version}\n"
        f"---\n"
    )
    try:
        with open(decisions_file, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        logger.error(f"Failed to append to decisions.md: {e}")
