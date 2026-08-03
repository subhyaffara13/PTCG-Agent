from typing import Any

def only_consist_of(
    var: Any, types: tuple[type, ...], allow_none: bool = False
) -> bool:
    mismatch_vars = find_mismatched_vars(var, types, allow_none=allow_none)
    return len(mismatch_vars) == 0

