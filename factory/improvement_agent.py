"""
factory/improvement_agent.py
Decides the improvement path based on eval_report.json.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from agents.base_agent import BaseAgent
from factory.improvement_agent_helpers import determine_escalation, append_decision

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
        self.original_rubric = self._load_rubric()
        
    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("ImprovementAgent does not receive routed packets")

    def _load_rubric(self) -> dict:
        path = self.skills_dir / "eval_rubric.json"
        if path.exists():
            try: return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e: logger.error(f"Failed to read eval_rubric.json: {e}")
        return {"contexts": {}}

    def improve(self, eval_report: dict) -> dict:
        action, reasoning, next_context = determine_escalation(eval_report)
        
        version_scores = eval_report.get("version_scores", {})
        best_version = version_scores.get("best_version", "player_b")
        iteration = eval_report.get("iteration", 0)

        notes = {
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "action_taken": action,
            "reasoning": reasoning,
            "next_eval_context": next_context,
            "weight_changes": None,
            "escalation": {
                "deck_architect": action in ("escalate_deck_architect", "escalate_both"),
                "builder_agent": action in ("escalate_builder_agent", "escalate_both")
            },
            "best_version_to_carry_forward": best_version
        }
        
        notes_file = self.log_dir / "improvement_notes.json"
        notes_file.write_text(json.dumps(notes, indent=2), encoding="utf-8")

        append_decision(self.decisions_file, iteration, action, reasoning, next_context, best_version)
        return notes
