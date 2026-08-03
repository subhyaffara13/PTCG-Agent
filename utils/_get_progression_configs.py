from typing import Any

def _get_progression_configs() -> list[dict[str, Any]]:
    # TODO make this configurable
    return [
        {"max_autotune": True},
    ]

