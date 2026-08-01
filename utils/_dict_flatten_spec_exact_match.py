
def _dict_flatten_spec_exact_match(d: dict[_K, _V], spec: TreeSpec) -> bool:
    return len(d) == spec.num_children

