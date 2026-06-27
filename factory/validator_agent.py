"""
factory/validator_agent.py
Enforces syntax correctness, inheritance bounds, security checks, and promotion logic.
"""
import os, json, shutil, logging
from datetime import datetime
from pathlib import Path
from typing import Any
from agents.base_agent import BaseAgent
from factory.teams.sanitization_team import SanitizationTeam
from factory.validator_helpers import load_baseline_score, handle_validation_failure, append_to_history, write_validation_log

logger = logging.getLogger(__name__)

class ValidatorAgent(BaseAgent):
    def __init__(self, log_dir="logs", versions_dir="versions", staging_dir="staging", 
                 agents_dir="agents", factory_dir="factory", perspective_flag="factory"):
        super().__init__(perspective_flag)
        self.log_dir, self.versions_dir, self.staging_dir = Path(log_dir), Path(versions_dir), Path(staging_dir)
        self.agents_dir, self.factory_dir = Path(agents_dir), Path(factory_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        self.validation_log_file = self.log_dir / "validation_log.json"
        self.history_file = self.versions_dir / "version_history.json"
        self.baseline_score = load_baseline_score(self.history_file)
        self.sanitization = SanitizationTeam()

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("ValidatorAgent does not receive routed packets")

    def validate(self, staged_file_path: str, eval_report: dict) -> dict:
        staged_path = Path(staged_file_path)
        timestamp = datetime.now().isoformat()
        version_id = f"v_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        checks = {k: "n/a" for k in ["syntax", "base_inheritance", "receive_method", "router_boundaries", "no_auto_submit", "no_api_keys", "time_compliance", "score_improvement", "staging_integrity"]}
        report = {"version_id": version_id, "timestamp": timestamp, "staged_file": str(staged_path), "checks": checks, "all_passed": False, "promoted": False, "failed_check": None, "reason": None}

        try: content = staged_path.read_text(encoding="utf-8")
        except Exception as e: return handle_validation_failure(report, 0, f"Could not read: {e}", self.validation_log_file)

        passed, err_msg = self.sanitization.validate_code(staged_path, content)
        if not passed: return handle_validation_failure(report, 1, err_msg, self.validation_log_file)
        for k in ["syntax", "base_inheritance", "receive_method", "router_boundaries", "no_auto_submit", "no_api_keys", "time_compliance"]:
            checks[k] = "pass"

        new_score = eval_report.get("version_scores", {}).get("player_b", 0.0)
        if new_score < self.baseline_score:
            return handle_validation_failure(report, 8, f"Score {new_score} fails baseline.", self.validation_log_file)
        checks["score_improvement"] = "pass"

        staged_abs = staged_path.resolve()
        if self.staging_dir.resolve() not in staged_abs.parents or self.agents_dir.resolve() in staged_abs.parents or self.factory_dir.resolve() in staged_abs.parents:
            return handle_validation_failure(report, 9, "Staged file path/integrity error", self.validation_log_file)
        checks["staging_integrity"] = "pass"

        is_factory = any(x in staged_path.name for x in ["logger", "runner", "eval", "improvement", "builder", "validator"])
        try: shutil.copy2(staged_path, (self.factory_dir if is_factory else self.agents_dir) / staged_path.name)
        except Exception as e: return handle_validation_failure(report, 9, f"Copy failed: {e}", self.validation_log_file)

        report.update({"all_passed": True, "promoted": True})
        self.baseline_score = new_score
        
        append_to_history(self.history_file, {
            "version_id": version_id, "timestamp": timestamp, "staged_file": str(staged_path),
            "version_score": new_score, "improvement_vs_baseline": round(new_score - self.baseline_score, 4),
            "checks_passed": 9, "promoted": True, "raw_scores": eval_report.get("raw_scores", {})
        })
        write_validation_log(report, self.validation_log_file)
        return report
