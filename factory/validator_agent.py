"""
factory/validator_agent.py

Enforces syntax correctness, inheritance bounds, security checks, time limits,
regression testing, and promotion logic prior to pushing staged updates live.
"""

import os
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from agents.base_agent import BaseAgent
from factory.validator_syntax import check_syntax_and_inheritance
from factory.validator_security import check_security_and_time

logger = logging.getLogger(__name__)

class ValidatorAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", versions_dir: str = "versions", 
                 staging_dir: str = "staging", agents_dir: str = "agents", 
                 factory_dir: str = "factory", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.versions_dir = Path(versions_dir)
        self.staging_dir = Path(staging_dir)
        self.agents_dir = Path(agents_dir)
        self.factory_dir = Path(factory_dir)
        self.skills_dir = Path("skills")
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        
        self.validation_log_file = self.log_dir / "validation_log.json"
        self.history_file = self.versions_dir / "version_history.json"
        self.baseline_score = self._load_baseline_score()

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("ValidatorAgent does not receive routed packets")

    def _load_baseline_score(self) -> float:
        if self.history_file.exists():
            try:
                history = json.loads(self.history_file.read_text(encoding="utf-8").strip())
                if history:
                    scores = [item.get("version_score", 0.0) for item in history if item.get("promoted") is True]
                    if scores: return max(scores)
            except Exception as e:
                logger.error(f"Failed to load baseline score: {e}")
        return 0.0

    def validate(self, staged_file_path: str, eval_report: dict) -> dict:
        staged_path = Path(staged_file_path)
        timestamp = datetime.now().isoformat()
        version_id = f"v_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        checks = {k: "n/a" for k in ["syntax", "base_inheritance", "receive_method", "router_boundaries", "no_auto_submit", "no_api_keys", "time_compliance", "score_improvement", "staging_integrity"]}
        report = {"version_id": version_id, "timestamp": timestamp, "staged_file": str(staged_path), "checks": checks, "all_passed": False, "promoted": False, "failed_check": None, "reason": None}

        try:
            content = staged_path.read_text(encoding="utf-8")
        except Exception as e:
            return self._handle_failure(report, 0, f"Could not read staged file: {e}")

        # Check 1, 2, 3 (Syntax and Structure)
        passed, err_msg = check_syntax_and_inheritance(staged_path, content, self.skills_dir)
        if not passed:
            check_num = 1 if "Syntax" in err_msg or "CSV" in err_msg or "Rule" in err_msg or "Basic" in err_msg else (2 if "BaseAgent" in err_msg else 3)
            return self._handle_failure(report, check_num, err_msg)
        for k in ["syntax", "base_inheritance", "receive_method"]:
            checks[k] = "pass"

        # Check 4, 5, 6, 7 (Security and Compliance)
        failed_check, sec_err = check_security_and_time(staged_path, content)
        if failed_check > 0:
            return self._handle_failure(report, failed_check, sec_err)
        for k in ["router_boundaries", "no_auto_submit", "no_api_keys"]:
            checks[k] = "pass"
        checks["time_compliance"] = "pass" if staged_path.name == "game_runner.py" else "n/a"

        # Check 8 (Version Score Improvement)
        new_score = eval_report.get("version_scores", {}).get("player_b", 0.0)
        if new_score < self.baseline_score:
            return self._handle_failure(report, 8, f"New score {new_score} fails baseline. Delta: {round(self.baseline_score - new_score, 4)}")
        checks["score_improvement"] = "pass"

        # Check 9 (Staging integrity)
        staged_abs = staged_path.resolve()
        if self.staging_dir.resolve() not in staged_abs.parents:
            return self._handle_failure(report, 9, f"Staged file must be in {self.staging_dir}")
        if self.agents_dir.resolve() in staged_abs.parents or self.factory_dir.resolve() in staged_abs.parents:
            return self._handle_failure(report, 9, "Staged file cannot reside in live directory path")
        checks["staging_integrity"] = "pass"

        # Promotion
        is_factory = any(x in staged_path.name for x in ["logger", "runner", "eval", "improvement", "builder", "validator"])
        dest_dir = self.factory_dir if is_factory else self.agents_dir
        try:
            shutil.copy2(staged_path, dest_dir / staged_path.name)
        except Exception as e:
            return self._handle_failure(report, 9, f"Copying staged file failed: {e}")

        report.update({"all_passed": True, "promoted": True})
        self.baseline_score = new_score
        
        self._append_to_history({
            "version_id": version_id, "timestamp": timestamp, "staged_file": str(staged_path),
            "version_score": new_score, "improvement_vs_baseline": round(new_score - self.baseline_score, 4),
            "checks_passed": 9, "promoted": True, "raw_scores": eval_report.get("raw_scores", {})
        })
        self._write_validation_log(report)
        return report

    def _handle_failure(self, report: dict, check_num: int, reason: str) -> dict:
        report.update({"all_passed": False, "promoted": False, "failed_check": f"check_{check_num}", "reason": reason})
        check_mapping = {1: "syntax", 2: "base_inheritance", 3: "receive_method", 4: "router_boundaries", 5: "no_auto_submit", 6: "no_api_keys", 7: "time_compliance", 8: "score_improvement", 9: "staging_integrity"}
        name = check_mapping.get(check_num)
        if name: report["checks"][name] = "fail"
        self._write_validation_log(report)
        return report

    def _append_to_history(self, record: dict):
        history = []
        if self.history_file.exists():
            try:
                history = json.loads(self.history_file.read_text(encoding="utf-8").strip())
            except Exception as e:
                logger.error(f"Failed to read version history: {e}")
        history.append(record)
        try:
            self.history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to write version history: {e}")

    def _write_validation_log(self, report: dict):
        try:
            self.validation_log_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to write validation log: {e}")
