
def elevate_quadratic(p0, p1, p2):
    """Given a quadratic bezier curve, return its degree-elevated cubic."""

    # https://pomax.github.io/bezierinfo/#reordering
    p1_2_3 = p1 * (2 / 3)
    return (
        p0,
        (p0 * (1 / 3) + p1_2_3),
        (p2 * (1 / 3) + p1_2_3),
        p2,
    )

