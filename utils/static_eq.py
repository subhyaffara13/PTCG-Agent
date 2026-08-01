
def static_eq(a: _IntLike, b: _IntLike) -> bool:
    return V.graph.sizevars.statically_known_equals(a, b)

