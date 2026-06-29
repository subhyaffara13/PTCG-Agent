import gzip
import base64
import json
import logging
from pathlib import Path

logger = logging.getLogger("telemetry_sync")

def compress_telemetry(res_dict: dict, log_dir: str = "logs") -> dict:
    """Finds steps_*.json files in res_dict, compresses them to base64 gzipped strings, and deletes local copies."""
    telemetry_data = {}
    log_path = Path(log_dir)
    
    games = res_dict.get("games", {})
    for game_label, game_data in games.items():
        # Only look at individual parallel games, not aggregated ones
        if not any(game_label.startswith(p) for p in ["deck_test_", "variance_baseline_"]):
            continue
            
        log_files = game_data.get("log_files", {})
        steps_filename = log_files.get("steps")
        if not steps_filename:
            continue
            
        file_path = log_path / steps_filename
        if file_path.exists():
            try:
                content = file_path.read_bytes()
                compressed = gzip.compress(content)
                encoded = base64.b64encode(compressed).decode('utf-8')
                telemetry_data[steps_filename] = encoded
                
                # Delete local file on worker to save space
                file_path.unlink()
            except Exception as e:
                logger.error(f"Failed to compress telemetry file {steps_filename}: {e}")
                
    return telemetry_data

def decompress_telemetry(telemetry_data: dict, log_dir: str = "logs"):
    """Decompresses telemetry data and writes steps_*.json files to the specified log directory."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    for filename, b64_gzip_str in telemetry_data.items():
        file_path = log_path / filename
        try:
            compressed = base64.b64decode(b64_gzip_str.encode('utf-8'))
            decompressed = gzip.decompress(compressed)
            file_path.write_bytes(decompressed)
            logger.info(f"Decompressed and saved telemetry: {filename}")
        except Exception as e:
            logger.error(f"Failed to decompress telemetry file {filename}: {e}")
