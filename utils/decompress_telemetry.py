from pathlib import Path


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

