
def broadcastable(shape_a: tuple[int, ...], shape_b: tuple[int, ...]) -> bool:
    """Check if two shapes are broadcastable."""
    return all(
        (m == n) or (m == 1) or (n == 1) for m, n in zip(shape_a[::-1], shape_b[::-1])
    )

