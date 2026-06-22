"""
factory/builder_agent.py

Modifies exactly ONE target component in the allowed list, outputs to staging/,
and logs the change to decisions.md.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from agents.base_agent import BaseAgent
import factory.builder_helper as helper

logger = logging.getLogger(__name__)

class BuilderAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", staging_dir: str = "staging", 
                 decisions_file: str = "decisions.md", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.staging_dir = Path(staging_dir)
        self.decisions_file = Path(decisions_file)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        
        self.allowed_targets = [
            "agents/hand_analyst.py", "agents/turn_planner.py",
            "agents/strategy_agent.py", "agents/opponent_model.py",
            "skills/priority_rules.json", "skills/strategy_profiles.json"
        ]

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("BuilderAgent does not receive routed packets")

    def build(self, improvement_notes: dict) -> dict:
        escalation = improvement_notes.get("escalation", {})
        target_component = escalation.get("target", "agents/strategy_agent.py")
        weak_metric = improvement_notes.get("action_taken", "logic_delta")
        iteration = improvement_notes.get("iteration", 0)

        if target_component not in self.allowed_targets:
            helper.log_error_to_decisions(self.decisions_file, f"Target '{target_component}' is not in allowed list.")
            return {"status": "failed", "reason": "unauthorized_target"}

        target_path = Path(target_component)
        if not target_path.exists():
            helper.log_error_to_decisions(self.decisions_file, f"Target file '{target_component}' does not exist.")
            return {"status": "failed", "reason": "target_missing"}

        content = target_path.read_text(encoding="utf-8")
        change_type = ("reasoning_logic" if "logic_delta" in weak_metric.lower() else (
            "priority_rules" if "prize_efficiency" in weak_metric.lower() else (
                "ko_logic" if "ko_rate" in weak_metric.lower() else None
            )
        ))

        if not change_type:
            helper.log_error_to_decisions(self.decisions_file, "No clear change pattern from weak metric.")
            return {"status": "failed", "reason": "no_clear_change"}

        try:
            if target_path.suffix == ".json":
                mod_content, lines_modified, change_desc = helper.modify_json(content, change_type)
            else:
                mod_content, lines_modified, change_desc = helper.modify_python(content, change_type)
        except Exception as e:
            helper.log_error_to_decisions(self.decisions_file, f"Failed to edit file: {e}")
            return {"status": "failed", "reason": f"edit_error: {e}"}

        staged_dest = self.staging_dir / target_path.name
        staged_dest.write_text(mod_content, encoding="utf-8")

        report = {
            "timestamp": datetime.now().isoformat(), "target_component": target_component,
            "change_type": change_type, "weak_metric_addressed": weak_metric,
            "change_description": change_desc, "lines_modified": lines_modified,
            "staging_path": str(staged_dest)
        }
        (self.staging_dir / "build_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        
        helper.log_decision(self.decisions_file, iteration, target_component, change_type, weak_metric, change_desc, lines_modified)
        return {"status": "success", "target": target_component, "change_type": change_type, "staging_path": str(staged_dest)}
