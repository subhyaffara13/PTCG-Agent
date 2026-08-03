from typing import Any

def _get_autocast_states() -> list[Any]:
    return [
        torch.is_autocast_enabled("cuda"),
        torch.is_autocast_enabled("cpu"),
        torch.get_autocast_dtype("cuda"),
        torch.get_autocast_dtype("cpu"),
        torch.is_autocast_cache_enabled(),
    ]

