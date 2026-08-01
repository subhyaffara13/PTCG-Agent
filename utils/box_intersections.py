
def box_intersections(z, d, lb, ub,
                      entire_line=False):
    """Find the intersection between segment (or line) and box constraints.

    Find the intersection between the segment (or line) defined by the
    parametric  equation ``x(t) = z + t*d`` and the rectangular box
    ``lb <= x <= ub``.

    Parameters
    ----------
    z : array_like, shape (n,)
        Initial point.
    d : array_like, shape (n,)
        Direction.
    lb : array_like, shape (n,)
        Lower bounds to each one of the components of ``x``. Used
        to delimit the rectangular box.
    ub : array_like, shape (n, )
        Upper bounds to each one of the components of ``x``. Used
        to delimit the rectangular box.
    entire_line : bool, optional
        When ``True``, the function returns the intersection between the line
        ``x(t) = z + t*d`` (``t`` can assume any value) and the rectangular
        box. When ``False``, the function returns the intersection between the segment
        ``x(t) = z + t*d``, ``0 <= t <= 1``, and the rectangular box.

    Returns
    -------
    ta, tb : float
        The line/segment ``x(t) = z + t*d`` is inside the box for
        for ``ta <= t <= tb``.
    intersect : bool
        When ``True``, there is an intersection between the line (or segment)
        and the rectangular box. On the other hand, when ``False``, there is no
        intersection.
    """
    # Make sure it is a numpy array
    z = np.asarray(z)
    d = np.asarray(d)
    lb = np.asarray(lb)
    ub = np.asarray(ub)
    # Special case when d=0
    if norm(d) == 0:
        return 0, 0, False

    # Get values for which d==0
    zero_d = (d == 0)
    # If the boundaries are not satisfied for some coordinate
    # for which "d" is zero, there is no box-line intersection.
    if (z[zero_d] < lb[zero_d]).any() or (z[zero_d] > ub[zero_d]).any():
        intersect = False
        return 0, 0, intersect
    # Remove values for which d is zero
    not_zero_d = np.logical_not(zero_d)
    z = z[not_zero_d]
    d = d[not_zero_d]
    lb = lb[not_zero_d]
    ub = ub[not_zero_d]

    # Find a series of intervals (t_lb[i], t_ub[i]).
    t_lb = (lb-z) / d
    t_ub = (ub-z) / d
    # Get the intersection of all those intervals.
    ta = max(np.minimum(t_lb, t_ub))
    tb = min(np.maximum(t_lb, t_ub))

    # Check if intersection is feasible
    if ta <= tb:
        intersect = True
    else:
        intersect = False
    # Checks to see if intersection happens within vectors length.
    if not entire_line:
        if tb < 0 or ta > 1:
            intersect = False
            ta = 0
            tb = 0
        else:
            # Restrict intersection interval between 0 and 1.
            ta = max(0, ta)
            tb = min(1, tb)

    return ta, tb, intersect

