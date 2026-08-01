
def baddbmm_adapter(
    shapes: tuple[Any], concrete: tuple[Any]
) -> tuple[tuple[Any], dict[Any, Any]]:
    tmp = list(shapes)[:3]
    return tuple(tmp), {}

