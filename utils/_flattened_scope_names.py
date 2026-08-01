
def _flattened_scope_names(
    iterator: Iterator[nodes.Global | nodes.Nonlocal],
) -> set[str]:
    values = (set(stmt.names) for stmt in iterator)
    return set(itertools.chain.from_iterable(values))

