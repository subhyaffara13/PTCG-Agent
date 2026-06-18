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
        flag_deck_architect = eval_report["flags"]["flag_deck_architect"]
        flag_builder_agent = eval_report["flags"]["flag_builder_agent"]
        recommendation = eval_report["recommendation"]
        logic_delta = eval_report["metrics"]["logic_delta"]
        deck_delta = eval_report["metrics"]["deck_delta"]
        best_version = eval_report["version_scores"]["best_version"]
        eval_context = eval_report["eval_context"]
        iteration = eval_report.get("iteration", 0)

        action = "tuned_weights"
        reasoning = "Normal operation. Tuning weights."
        weight_changes = None
        renormalized = False

        # PRIORITY 1: Weight tuning (tune weights when recommended or default fallback)
        if recommendation == "tune":
            rubric = self._load_rubric()
            context_weights = rubric.get("contexts", {}).get(eval_context, {})
            original_weights = self.original_rubric.get("contexts", {}).get(eval_context, {})

            changes = {}
            if logic_delta < 0.1 and "logic_delta" in context_weights:
                curr = context_weights["logic_delta"]
                orig = original_weights.get("logic_delta", curr)
                if curr + self.tweak_step <= orig + self.max_tweak:
                    context_weights["logic_delta"] += self.tweak_step
                    changes["logic_delta"] = f"+{self.tweak_step}"

            if deck_delta < 0.1 and "prize_efficiency" in context_weights:
                curr = context_weights["prize_efficiency"]
                orig = original_weights.get("prize_efficiency", curr)
                if curr + self.tweak_step <= orig + self.max_tweak:
                    context_weights["prize_efficiency"] += self.tweak_step
                    changes["prize_efficiency"] = f"+{self.tweak_step}"

            # Renormalize context weights to sum to 1.0
            if changes:
                total = sum(context_weights.values())
                if total > 0:
                    for k in context_weights:
                        context_weights[k] /= total
                    renormalized = True
                
                weight_changes = {eval_context: context_weights}
                reasoning = f"Tuned weights: {changes} in context '{eval_context}'."
                if renormalized:
                    reasoning += " Weights renormalized to sum to 1.0."

                # Write back changes
                rubric_file = self.skills_dir / "eval_rubric.json"
                rubric_file.write_text(json.dumps(rubric, indent=2), encoding="utf-8")

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
