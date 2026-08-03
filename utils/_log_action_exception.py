import json
from pathlib import Path


def _log_action_exception(exc: Exception):
    try:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "action_log.json"
        
        error_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "submission_agent_crash",
            "agent_called": "submission/main.py",
            "packet_type": "exception",
            "error_reason": str(exc)
        }
        
        logs = []
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8").strip()
            if content:
                try:
                    logs = json.loads(content)
                    if not isinstance(logs, list):
                        logs = [logs]
                except json.JSONDecodeError:
                    logs = []
        logs.append(error_entry)
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    except Exception as log_err:
        pass


def _log_action_exception(exc: Exception):
    try:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "action_log.json"
        
        error_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "submission_agent_crash",
            "agent_called": "submission/main.py",
            "packet_type": "exception",
            "error_reason": str(exc)
        }
        
        logs = []
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8").strip()
            if content:
                try:
                    logs = json.loads(content)
                    if not isinstance(logs, list):
                        logs = [logs]
                except json.JSONDecodeError:
                    logs = []
        logs.append(error_entry)
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    except Exception as log_err:
        pass


def _log_action_exception(exc: Exception):
    try:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "action_log.json"
        
        error_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "submission_agent_crash",
            "agent_called": "submission/main.py",
            "packet_type": "exception",
            "error_reason": str(exc)
        }
        
        logs = []
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8").strip()
            if content:
                try:
                    logs = json.loads(content)
                    if not isinstance(logs, list):
                        logs = [logs]
                except json.JSONDecodeError:
                    logs = []
        logs.append(error_entry)
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    except Exception as log_err:
        pass


def _log_action_exception(exc: Exception):
    try:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "action_log.json"
        
        error_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "submission_agent_crash",
            "agent_called": "submission/main.py",
            "packet_type": "exception",
            "error_reason": str(exc)
        }
        
        logs = []
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8").strip()
            if content:
                try:
                    logs = json.loads(content)
                    if not isinstance(logs, list):
                        logs = [logs]
                except json.JSONDecodeError:
                    logs = []
        logs.append(error_entry)
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    except Exception as log_err:
        pass

