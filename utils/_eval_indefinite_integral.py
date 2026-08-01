
def _eval_indefinite_integral(F, a, b, xp):
    """
    Calculates a definite integral from points `a` to `b` by summing up over the corners
    of the corresponding hyperrectangle.
    """

    ndim = xp_size(a)
    points = xp.stack([a, b], axis=0)

    out = 0
    for ind in itertools.product(range(2), repeat=ndim):
        selected_points = xp.asarray(
            [float(points[i, j]) for i, j in zip(ind, range(ndim))]
        )
        out += pow(-1, sum(ind) + ndim) * F(selected_points)

    return out

