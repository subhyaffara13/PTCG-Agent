import json
from pathlib import Path


def _write_cached_registry(path: str, registry: Registry) -> None:
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(registry, f)
    except Exception:
        logger.debug("Could not cache agent harnesses registry.", exc_info=True)

