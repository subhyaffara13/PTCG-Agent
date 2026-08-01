
def _tuple_flatten_spec_exact_match(d: tuple[_T, ...], spec: TreeSpec) -> bool:
    return len(d) == spec.num_children

