"""
factory/validator_agent.py

Enforces syntax correctness, inheritance bounds, security checks, time limits,
regression testing, and promotion logic prior to pushing staged updates live.
"""

import ast
import os
import re
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple
from agents.base_agent import BaseAgent

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
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        
        self.validation_log_file = self.log_dir / "validation_log.json"
        self.history_file = self.versions_dir / "version_history.json"
        
        self.time_limit = 600
        self.min_improvement = 0.0
        
        # Load previous baseline
        self.baseline_score = self._load_baseline_score()

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "ValidatorAgent does not receive routed packets — it validates codebase components directly"
        )

    def _load_baseline_score(self) -> float:
        if self.history_file.exists():
            try:
                content = self.history_file.read_text(encoding="utf-8").strip()
                if content:
                    history = json.loads(content)
                    if isinstance(history, list) and history:
                        # Extract maximum promoted version score as baseline
                        scores = [item.get("version_score", 0.0) for item in history if item.get("promoted") is True]
                        if scores:
                            return max(scores)
            except Exception as e:
                logger.error(f"Failed to load baseline score: {e}")
        return 0.0

    def validate(self, staged_file_path: str, eval_report: dict) -> dict:
        """
        Runs exactly 9 checks in strict sequence. Promotes or logs failure.
        """
        staged_path = Path(staged_file_path)
        timestamp = datetime.now().isoformat()
        version_id = f"v_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        checks_status = {
            "syntax": "n/a", "base_inheritance": "n/a", "receive_method": "n/a",
            "router_boundaries": "n/a", "no_auto_submit": "n/a", "no_api_keys": "n/a",
            "time_compliance": "n/a", "score_improvement": "n/a", "staging_integrity": "n/a"
        }

        # Initialize failure/success payload template
        report = {
            "version_id": version_id,
            "timestamp": timestamp,
            "staged_file": str(staged_path),
            "checks": checks_status,
            "all_passed": False,
            "promoted": False,
            "failed_check": None,
            "reason": None
        }

        try:
            content = staged_path.read_text(encoding="utf-8")
        except Exception as e:
            return self._handle_failure(report, 0, f"Could not read staged file: {e}")

        # --- CHECK 1: Python Syntax ---
        checks_status["syntax"] = "fail"
        try:
            tree = ast.parse(content, filename=staged_path.name)
            checks_status["syntax"] = "pass"
        except SyntaxError as e:
            return self._handle_failure(report, 1, f"SyntaxError on line {e.lineno}: {e.msg}")

        # --- CHECK 2: BaseAgent Inheritance ---
        checks_status["base_inheritance"] = "fail"
        has_class = False
        inherits_base = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                has_class = True
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "BaseAgent":
                        inherits_base = True
                        break
        if has_class and not inherits_base:
            return self._handle_failure(report, 2, "Class definition found but does not inherit from BaseAgent")
        checks_status["base_inheritance"] = "pass"

        # --- CHECK 3: receive() NotImplementedError ---
        checks_status["receive_method"] = "fail"
        is_factory = any(x in staged_path.name for x in ["logger", "runner", "eval", "improvement", "builder", "validator"])
        has_receive = False
        receive_raises_nie = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "receive":
                has_receive = True
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Raise):
                        if isinstance(sub_node.exc, ast.Call) and isinstance(sub_node.exc.func, ast.Name) and sub_node.exc.func.id == "NotImplementedError":
                            receive_raises_nie = True
                        elif isinstance(sub_node.exc, ast.Name) and sub_node.exc.id == "NotImplementedError":
                            receive_raises_nie = True
        
        if is_factory:
            if not has_receive or not receive_raises_nie:
                return self._handle_failure(report, 3, "Factory component receive() must raise NotImplementedError")
        else:
            if not has_receive:
                return self._handle_failure(report, 3, "Player agent receive() is missing or not implemented")
        checks_status["receive_method"] = "pass"

        # --- CHECK 4: Router Bus Boundaries ---
        checks_status["router_boundaries"] = "fail"
        lines = content.splitlines()
        for idx, line in enumerate(lines, start=1):
            if "GameState" in line or "OrchestratorState" in line:
                return self._handle_failure(report, 4, f"Access to full state object found on line {idx}")
            if "RouterBus." in line and not (".dispatch(" in line):
                return self._handle_failure(report, 4, f"Direct access to RouterBus internals on line {idx}")
        checks_status["router_boundaries"] = "pass"

        # --- CHECK 5: No Auto-Submit Logic ---
        checks_status["no_auto_submit"] = "fail"
        forbidden_words = ["kaggle", "submit", "api_key", "upload", "competition"]
        for idx, line in enumerate(lines, start=1):
            for word in forbidden_words:
                if word in line.lower():
                    # Ignore normal python imports, path configs, or strings containing keywords in comments
                    if f"#{word}" not in line.lower() and "import" not in line.lower():
                        return self._handle_failure(report, 5, f"Auto-submit string '{word}' found on line {idx}")
        checks_status["no_auto_submit"] = "pass"

        # --- CHECK 6: No Hardcoded API Keys ---
        checks_status["no_api_keys"] = "fail"
        key_pattern = re.compile(r'["\'](sk-[A-Za-z0-9]{15,}|AIza[A-Za-z0-9_-]{15,}|Bearer\s+[A-Za-z0-9_-]{15,})["\']')
        long_string_pattern = re.compile(r'["\']([A-Za-z0-9]{20,})["\']')
        
        for idx, line in enumerate(lines, start=1):
            match = key_pattern.search(line)
            if match:
                redacted_val = "[REDACTED]"
                return self._handle_failure(report, 6, f"Hardcoded key pattern found on line {idx}: {redacted_val}")
            
            # Simple check for strings longer than 20 chars with a mix of characters
            for match in long_string_pattern.finditer(line):
                val = match.group(1)
                # If mixed casing and digits exist, flag it
                if any(c.islower() for c in val) and any(c.isupper() for c in val) and any(c.isdigit() for c in val):
                    redacted_val = "[REDACTED]"
                    return self._handle_failure(report, 6, f"Suspected high-entropy key on line {idx}: {redacted_val}")
        checks_status["no_api_keys"] = "pass"

        # --- CHECK 7: Time Limit Compliance ---
        if staged_path.name == "game_runner.py":
            checks_status["time_compliance"] = "fail"
            # Ensure safety levels exist
            if not any("600" in line for line in lines):
                return self._handle_failure(report, 7, "Forced game timeout (600s) check missing in game_runner.py")
            if not any("540" in line for line in lines):
                return self._handle_failure(report, 7, "Fastest legal move check at 540s missing in game_runner.py")
            if not any("570" in line for line in lines):
                return self._handle_failure(report, 7, "Forced pass check at 570s missing in game_runner.py")
            checks_status["time_compliance"] = "pass"
        else:
            checks_status["time_compliance"] = "n/a"

        # --- CHECK 8: Version Score Improvement ---
        checks_status["score_improvement"] = "fail"
        new_score = eval_report.get("version_scores", {}).get("player_b", 0.0)
        if new_score < self.baseline_score:
            delta = self.baseline_score - new_score
            return self._handle_failure(report, 8, f"New score {new_score} fails baseline check. Delta: {round(delta, 4)}")
        checks_status["score_improvement"] = "pass"

        # --- CHECK 9: Staging Directory Integrity ---
        checks_status["staging_integrity"] = "fail"
        staged_abs = staged_path.resolve()
        
        # Ensure it is placed in staging folder
        if self.staging_dir.resolve() not in staged_abs.parents:
            return self._handle_failure(report, 9, f"Staged file must be in {self.staging_dir}")
        
        # Prevent any live agent pushes
        if self.agents_dir.resolve() in staged_abs.parents or self.factory_dir.resolve() in staged_abs.parents:
            return self._handle_failure(report, 9, "Staged file cannot reside in live directory path")
        checks_status["staging_integrity"] = "pass"

        # --- PROMOTION ---
        # All checks passed! Execute copying and logs.
        dest_dir = self.factory_dir if is_factory else self.agents_dir
        dest_path = dest_dir / staged_path.name
        
        try:
            shutil.copy2(staged_path, dest_path)
        except Exception as e:
            return self._handle_failure(report, 9, f"Copying staged file to live location failed: {e}")

        report["all_passed"] = True
        report["promoted"] = True
        
        self.baseline_score = new_score
        
        # Write to version_history.json
        self._append_to_history({
            "version_id": version_id,
            "timestamp": timestamp,
            "staged_file": str(staged_path),
            "version_score": new_score,
            "improvement_vs_baseline": round(new_score - self.baseline_score, 4),
            "checks_passed": 9,
            "promoted": True
        })

        # Write to validation_log.json
        self._write_validation_log(report)
        return report

    def _handle_failure(self, report: dict, check_num: int, reason: str) -> dict:
        """Helper to format report on any fail and serialize metadata."""
        report["all_passed"] = False
        report["promoted"] = False
        report["failed_check"] = f"check_{check_num}"
        report["reason"] = reason

        # Log check status fail if matching check_num
        check_mapping = {
            1: "syntax", 2: "base_inheritance", 3: "receive_method",
            4: "router_boundaries", 5: "no_auto_submit", 6: "no_api_keys",
            7: "time_compliance", 8: "score_improvement", 9: "staging_integrity"
        }
        name = check_mapping.get(check_num)
        if name:
            report["checks"][name] = "fail"

        # Write to version_history.json
        self._append_to_history({
            "version_id": report["version_id"],
            "timestamp": report["timestamp"],
            "staged_file": report["staged_file"],
            "version_score": 0.0,
            "failed_check": check_num,
            "reason": reason,
            "promoted": False
        })

        # Write to validation_log.json
        self._write_validation_log(report)
        return report

    def _append_to_history(self, record: dict):
        history = []
        if self.history_file.exists():
            try:
                content = self.history_file.read_text(encoding="utf-8").strip()
                if content:
                    history = json.loads(content)
                    if not isinstance(history, list):
                        history = [history]
            except Exception:
                pass
        history.append(record)
        self.history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")

    def _write_validation_log(self, report: dict):
        logs = []
        if self.validation_log_file.exists():
            try:
                content = self.validation_log_file.read_text(encoding="utf-8").strip()
                if content:
                    logs = json.loads(content)
                    if not isinstance(logs, list):
                        logs = [logs]
            except Exception:
                pass
        logs.append(report)
        self.validation_log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
