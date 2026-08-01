
def _dict_flatten_spec(d: dict[_K, _V], spec: TreeSpec) -> list[_V]:
    return [d[k] for k in spec.context]

