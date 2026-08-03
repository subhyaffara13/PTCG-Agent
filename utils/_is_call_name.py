import re

def _is_call_name(call_name: str, base: str) -> bool:
    # Recognize when call_name = _call_name(base, n) for some n >= 0.
    return re.match(re.escape(base) + r"(@\d+)?$", call_name) is not None

