from typing import Any

def iter_router_fallback_model_names(fallbacks: Any) -> Iterator[str]:
    """Yield leaf model names from any of the supported fallbacks shapes.

    Handles the simple top-level shape (``str`` or ``{"model": str}``) and
    the nested router-config shape (``[{primary: [fallback_list]}]``).
    """
    if not isinstance(fallbacks, list):
        return
    for entry in fallbacks:
        if isinstance(entry, str):
            yield entry
        elif isinstance(entry, dict):
            if isinstance(entry.get("model"), str):
                yield entry["model"]
                continue
            for fallback_list in entry.values():
                if not isinstance(fallback_list, list):
                    continue
                for m in fallback_list:
                    if isinstance(m, str):
                        yield m
                    elif isinstance(m, dict) and isinstance(m.get("model"), str):
                        yield m["model"]

