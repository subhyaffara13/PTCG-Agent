
def round_start_circle_stable_containment(c0, r0, c1, r1):
    """Round start circle so that it stays inside/outside end circle after rounding.

    The rounding of circle coordinates to integers may cause an abrupt change
    if the start circle c0 is so close to the end circle c1's perimiter that
    it ends up falling outside (or inside) as a result of the rounding.
    To keep the gradient unchanged, we nudge it in the right direction.

    See:
    https://github.com/googlefonts/colr-gradients-spec/issues/204
    https://github.com/googlefonts/picosvg/issues/158
    """
    start, end = Circle(c0, r0), Circle(c1, r1)

    inside_before_round = start.inside(end)

    round_start = start.round()
    round_end = end.round()
    inside_after_round = round_start.inside(round_end)

    if inside_before_round == inside_after_round:
        return round_start
    elif inside_after_round:
        # start was outside before rounding: we need to push start away from end
        direction = _vector_between(round_end.centre, round_start.centre)
        radius_delta = +1.0
    else:
        # start was inside before rounding: we need to push start towards end
        direction = _vector_between(round_start.centre, round_end.centre)
        radius_delta = -1.0
    dx, dy = _rounding_offset(direction)

    # At most 2 iterations ought to be enough to converge. Before the loop, we
    # know the start circle didn't keep containment after normal rounding; thus
    # we continue adjusting by -/+ 1.0 until containment is restored.
    # Normal rounding can at most move each coordinates -/+0.5; in the worst case
    # both the start and end circle's centres and radii will be rounded in opposite
    # directions, e.g. when they move along a 45 degree diagonal:
    #   c0 = (1.5, 1.5) ===> (2.0, 2.0)
    #   r0 = 0.5 ===> 1.0
    #   c1 = (0.499, 0.499) ===> (0.0, 0.0)
    #   r1 = 2.499 ===> 2.0
    # In this example, the relative distance between the circles, calculated
    # as r1 - (r0 + distance(c0, c1)) is initially 0.57437 (c0 is inside c1), and
    # -1.82842 after rounding (c0 is now outside c1). Nudging c0 by -1.0 on both
    # x and y axes moves it towards c1 by hypot(-1.0, -1.0) = 1.41421. Two of these
    # moves cover twice that distance, which is enough to restore containment.
    max_attempts = 2
    for _ in range(max_attempts):
        if round_start.concentric(round_end):
            # can't move c0 towards c1 (they are the same), so we change the radius
            round_start.radius += radius_delta
            assert round_start.radius >= 0
        else:
            round_start.move(dx, dy)
        if inside_before_round == round_start.inside(round_end):
            break
    else:  # likely a bug
        raise AssertionError(
            f"Rounding circle {start} "
            f"{'inside' if inside_before_round else 'outside'} "
            f"{end} failed after {max_attempts} attempts!"
        )

    return round_start

