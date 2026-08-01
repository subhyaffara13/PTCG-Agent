
def _getscaleoffset(
    expr: Callable[[ImagePointTransform], ImagePointTransform | float],
) -> tuple[float, float]:
    a = expr(ImagePointTransform(1, 0))
    return (a.scale, a.offset) if isinstance(a, ImagePointTransform) else (0, a)

