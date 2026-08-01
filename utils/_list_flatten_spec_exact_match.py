
def _list_flatten_spec_exact_match(d: list[_T], spec: TreeSpec) -> bool:
    return len(d) == spec.num_children

