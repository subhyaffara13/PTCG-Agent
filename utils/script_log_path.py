from pathlib import Path

def script_log_path(script: str) -> str:
    return f"logs/{Path(script).stem}.log"
