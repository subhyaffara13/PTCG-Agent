
def isset(x: object) -> TypeGuard[set[object] | frozenset[object]]:
    return isinstance(x, set | frozenset)

