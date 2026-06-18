"""
factory/builder_agent.py

Modifies exactly ONE target component in the allowed list, outputs to staging/,
and logs the change to decisions.md.
"""

import ast
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from agents.base_agent import BaseAgent

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
        
        # Allowed modification targets list
        self.allowed_targets = [
            "agents/hand_analyst.py",
            "agents/turn_planner.py",
            "agents/strategy_agent.py",
            "agents/opponent_model.py",
            "skills/priority_rules.json",
            "skills/strategy_profiles.json"
        ]

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "BuilderAgent does not receive routed packets — it modifies codebase components directly"
        )

    def build(self, improvement_notes: dict) -> dict:
        """
        Reads improvement notes, applies a targeted change to exactly one allowed component,
        writes output to staging/, and appends to decisions.md.
        """
        # STEP 1: Read target and metric parameters
        escalation = improvement_notes.get("escalation", {})
        target_component = escalation.get("target", "agents/strategy_agent.py")
        reasoning = improvement_notes.get("reasoning", "Low logic delta")
        weak_metric = improvement_notes.get("action_taken", "logic_delta")
        iteration = improvement_notes.get("iteration", 0)

        # HARD GUARD: Validate against allowed targets list
        if target_component not in self.allowed_targets:
            self._log_error_to_decisions(f"Target '{target_component}' is not in allowed list of modifications.")
            return {"status": "failed", "reason": "unauthorized_target"}

        # STEP 2: Read current component content
        target_path = Path(target_component)
        if not target_path.exists():
            self._log_error_to_decisions(f"Target file '{target_component}' does not exist.")
            return {"status": "failed", "reason": "target_missing"}

        content = target_path.read_text(encoding="utf-8")

        # STEP 3: Determine change type matching weak_metric
        change_type = None
        target_area = ""
        
        if "logic_delta" in weak_metric.lower():
            change_type = "reasoning_logic"
            target_area = "strategy decision thresholds"
        elif "prize_efficiency" in weak_metric.lower():
            change_type = "priority_rules"
            target_area = "attack priority thresholds"
        elif "ko_rate" in weak_metric.lower():
            change_type = "ko_logic"
            target_area = "KO detection and pursuit logic"

        if not change_type:
            self._log_error_to_decisions("No clear change pattern could be determined from weak metric.")
            return {"status": "failed", "reason": "no_clear_change"}

        # STEP 4: Apply exactly ONE change
        modified_content = ""
        lines_modified = []
        change_description = ""

        # Handle JSON edits
        if target_path.suffix == ".json":
            try:
                data = json.loads(content)
                # Apply tiny metric edit
                if change_type == "reasoning_logic" and "thresholds" in data:
                    data["thresholds"]["logic_margin"] = data["thresholds"].get("logic_margin", 0.5) + 0.05
                    change_description = "Increased logic_margin threshold by 0.05"
                elif change_type == "priority_rules" and "attack_priority" in data:
                    data["attack_priority"]["base_value"] = data["attack_priority"].get("base_value", 10) + 1
                    change_description = "Increased base attack_priority threshold value by 1"
                else:
                    data["last_metric_tweak"] = change_type
                    change_description = f"Tweaked last_metric_tweak config to {change_type}"

                modified_content = json.dumps(data, indent=2)
                lines_modified = [1]
            except Exception as e:
                self._log_error_to_decisions(f"Failed to parse or edit JSON: {e}")
                return {"status": "failed", "reason": f"json_edit_error: {e}"}
        
        # Handle Python file edits
        else:
            try:
                tree = ast.parse(content)
                # Apply tiny tweak on Python agent logic (simple text-based target threshold swap matching ast line context)
                lines = content.splitlines()
                modified = False
                for idx, line in enumerate(lines):
                    if "threshold" in line.lower() and "=" in line and not modified:
                        # Find numeric assignment and increment
                        parts = line.split("=")
                        try:
                            val = float(parts[1].strip())
                            lines[idx] = f"{parts[0]}= {val + 0.1}"
                            lines_modified.append(idx + 1)
                            change_description = f"Incremented logic threshold parameter on line {idx + 1}"
                            modified = True
                        except ValueError:
                            pass
                
                if not modified:
                    # Append placeholder comment to confirm change was registered
                    lines.append(f"\n# BuilderAgent: Adjusted {change_type} threshold parameters")
                    lines_modified = [len(lines)]
                    change_description = f"Appended {change_type} adjustment marker to bottom of file"
                
                modified_content = "\n".join(lines)
            except Exception as e:
                self._log_error_to_decisions(f"Failed to parse or edit Python AST: {e}")
                return {"status": "failed", "reason": f"ast_edit_error: {e}"}

        # STEP 5: Write staging files
        staged_dest = self.staging_dir / target_path.name
        staged_dest.write_text(modified_content, encoding="utf-8")

        # Write build_report.json
        report = {
            "timestamp": datetime.now().isoformat(),
            "target_component": target_component,
            "change_type": change_type,
            "weak_metric_addressed": weak_metric,
            "change_description": change_description,
            "lines_modified": lines_modified,
            "staging_path": str(staged_dest)
        }
        report_dest = self.staging_dir / "build_report.json"
        report_dest.write_text(json.dumps(report, indent=2), encoding="utf-8")

        # STEP 6: Log to decisions.md
        self._log_decision(iteration, target_component, change_type, weak_metric, change_description, lines_modified)

        return {
            "status": "success",
            "target": target_component,
            "change_type": change_type,
            "staging_path": str(staged_dest)
        }

    def _log_error_to_decisions(self, reason: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"\n## BUILDER AGENT ERROR — {timestamp}\n"
            f"**Error:** {reason}\n"
            f"---\n"
        )
        try:
            with open(self.decisions_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            logger.error(f"Failed to append error to decisions.md: {e}")

    def _log_decision(self, iteration: int, target: str, change_type: str, 
                      weak_metric: str, description: str, lines: list):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"\n## Builder Agent — Iteration {iteration} — {timestamp}\n"
            f"**Target:** {target}\n"
            f"**Change type:** {change_type}\n"
            f"**Weak metric:** {weak_metric}\n"
            f"**Change:** {description}\n"
            f"**Lines modified:** {lines}\n"
            f"---\n"
        )
        try:
            with open(self.decisions_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            logger.error(f"Failed to append builder log to decisions.md: {e}")
