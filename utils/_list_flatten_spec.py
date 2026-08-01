
def _list_flatten_spec(d: list[_T], spec: TreeSpec) -> list[_T]:
    return [d[i] for i in range(spec.num_children)]

