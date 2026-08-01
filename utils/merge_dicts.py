
def merge_dicts(d1: dict[str, Any], d2: dict[str, Any]) -> None:
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, Mapping):
            merge_dicts(d1[k], dict(v))
        else:
            d1[k] = d2[k]


def merge_dicts(*dicts):
    """Merge dictionaries into a single dictionary."""
    return {x: d[x] for d in dicts for x in d}

