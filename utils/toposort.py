
def toposort(deps: dict[T, set[T]]) -> list[T]:
    """Topologically sort a dict from item to dependencies.

    This runs in O(V + E).
    """
    result = []
    visited: set[T] = set()

    def visit(item: T) -> None:
        if item in visited:
            return

        for child in deps[item]:
            visit(child)

        result.append(item)
        visited.add(item)

    for item in deps:
        visit(item)

    return result

