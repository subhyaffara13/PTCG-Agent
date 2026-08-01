
def _tuple_flatten_spec(d: tuple[_T, ...], spec: TreeSpec) -> list[_T]:
    return [d[i] for i in range(spec.num_children)]

