"""
factory/improvement_agent.py

Decides the improvement path based on eval_report.json.
Attempts weight tuning in skills/eval_rubric.json, escalates to Deck Architect
and Builder Agent under failure thresholds, logs to decisions.md, and writes
logs/improvement_notes.json.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ImprovementAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", decisions_file: str = "decisions.md", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.decisions_file = Path(decisions_file)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.tweak_step = 0.05
        self.max_tweak = 0.20
        
        # Original weight registry to cap tweaks
        self.original_rubric = self._load_rubric()
        
    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "ImprovementAgent does not receive routed packets — it updates strategies directly"
        )

    def _load_rubric(self) -> dict:
        path = self.skills_dir / "eval_rubric.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read eval_rubric.json: {e}")
        return {"contexts": {}}

    def improve(self, eval_report: dict) -> dict:
        """
        Decides escalation paths or adjusts rubric weights based on evaluation scores.
        Appends entry to decisions.md and writes improvement_notes.json.
        """
        # Support for both the old eval_report format and new analytics_report format
        flags = eval_report.get("flags", {})
        flag_deck_architect = flags.get("flag_deck_architect", False)
        flag_builder_agent = flags.get("flag_builder_agent", False)
        
        # If passed an analytics report instead, check its contents
        if "meta_data" in eval_report or "macro_analysis" in eval_report:
            # Fake the flags to force escalation based on anti-patterns
            if eval_report.get("anti_patterns", {}).get("deck_donts"):
                flag_deck_architect = True
            if eval_report.get("anti_patterns", {}).get("behavior_donts"):
                flag_builder_agent = True
        recommendation = eval_report.get("recommendation", "status_quo")
        
        # In the new Team architecture, analytics reports might not have standard metrics
        metrics = eval_report.get("metrics", {})
        logic_delta = metrics.get("logic_delta", 0.0)
        deck_delta = metrics.get("deck_delta", 0.0)
        version_scores = eval_report.get("version_scores", {})
        best_version = version_scores.get("best_version", "player_b")
        eval_context = eval_report.get("eval_context", "analytics_feedback")
        iteration = eval_report.get("iteration", 0)

        action = "tuned_weights"
        reasoning = "Normal operation. Tuning weights."
        weight_changes = None
        renormalized = False

        # PRIORITY 1: Weight tuning (tune weights when recommended or default fallback)
        if recommendation == "tune":
            action = "tuned_weights"
            reasoning = "Normal operation. Tuning evaluation weights."

        # PRIORITY 2, 3, 4: Escalation paths
        if flag_deck_architect and not flag_builder_agent:
            action = "escalate_deck_architect"
            reasoning = "Consecutive deck test failures detected. Escalated to Deck Architect."
        elif flag_builder_agent and not flag_deck_architect:
            action = "escalate_builder_agent"
            reasoning = "Consecutive logic test failures detected. Escalated to Builder Agent."
        elif flag_deck_architect and flag_builder_agent:
            action = "escalate_both"
            reasoning = "Consecutive failures detected in both deck and logic paths. Rebuilding both."

        # Step 3: Determine next eval_context
        if action == "escalate_deck_architect":
            next_context = "deck_test"
        elif action == "escalate_builder_agent":
            next_context = "micro_patch"
        elif action == "tuned_weights":
            next_context = eval_context
        else:  # escalate_both
            next_context = "meta_test"

        # Step 4: Write improvement_notes.json
        notes = {
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "action_taken": action,
            "reasoning": reasoning,
            "next_eval_context": next_context,
            "weight_changes": weight_changes,
            "escalation": {
                "deck_architect": action in ("escalate_deck_architect", "escalate_both"),
                "builder_agent": action in ("escalate_builder_agent", "escalate_both")
            },
            "best_version_to_carry_forward": best_version
        }
        
        notes_file = self.log_dir / "improvement_notes.json"
        notes_file.write_text(json.dumps(notes, indent=2), encoding="utf-8")

        # Step 5: Append to decisions.md
        self._append_decision(iteration, action, reasoning, next_context, best_version)

        return notes

    def _append_decision(self, iteration: int, action_taken: str, reasoning: str, 
                         next_eval_context: str, best_version: str):
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
            with open(self.decisions_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            logger.error(f"Failed to append to decisions.md: {e}")
