import json
from typing import Dict, List
from pathlib import Path


def save_log_streams(log_dir: Path, timestamp_str: str, v_player: str, v_opponent: str, 
                     action_logs: List[Dict], reasoning_logs: List[Dict], variance_logs: List[Dict]):
    base_name = f"game_{timestamp_str}_v{v_player}_vs_v{v_opponent}"
    
    stream_mappings = {
        "action": action_logs,
        "reasoning": reasoning_logs,
        "variance": variance_logs
    }
    
    for suffix, logs in stream_mappings.items():
        file_path = log_dir / f"{suffix}_{base_name}.json"
        existing_logs = []
        if file_path.exists():
            try:
                content = file_path.read_text(encoding="utf-8").strip()
                if content:
                    existing_logs = json.loads(content)
            except Exception as e:
                logger.error(f"Error reading existing log file {file_path}: {e}")
        
        existing_logs.extend(logs)
        file_path.write_text(json.dumps(existing_logs, indent=2), encoding="utf-8")

