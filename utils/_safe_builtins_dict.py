from typing import Any

def _safe_builtins_dict(builtins_dict: dict[str, Any]) -> dict[str, Any]:
    """Filter a builtins dict to only picklable entries for serialization."""
    import pickle

    result = {}
    for k, v in builtins_dict.items():
        try:
            pickle.dumps(v)
            result[k] = v
        except Exception:
            pass
    return result

