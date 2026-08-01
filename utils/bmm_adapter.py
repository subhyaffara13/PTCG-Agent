
def bmm_adapter(
    shapes: tuple[Any], concrete: tuple[Any]
) -> tuple[tuple[Any], dict[Any, Any]]:
    tmp = list(shapes)
    return tuple(tmp[:2]), {}

