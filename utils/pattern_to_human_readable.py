from typing import Any

def pattern_to_human_readable(p) -> Any:
    if isinstance(p, tuple):
        # nested patterns, recurse
        return tuple(pattern_to_human_readable(inner_p) for inner_p in p)
    elif isinstance(p, str):
        # method names are already human readable
        return p
    else:
        p = remove_boolean_dispatch_from_name(p)
        return p

