
def iup_contour_optimize(
    deltas: _DeltaSegment, coords: _PointSegment, tolerance: Real = 0.0
) -> _DeltaOrNoneSegment:
    """For contour with coordinates `coords`, optimize a set of delta
    values `deltas` within error `tolerance`.

    Returns delta vector that has most number of None items instead of
    the input delta.
    """

    n = len(deltas)

    # Get the easy cases out of the way:

    # If all are within tolerance distance of 0, encode nothing:
    if all(abs(complex(*p)) <= tolerance for p in deltas):
        return [None] * n

    # If there's exactly one point, return it:
    if n == 1:
        return deltas

    # If all deltas are exactly the same, return just one (the first one):
    d0 = deltas[0]
    if all(d0 == d for d in deltas):
        return [d0] + [None] * (n - 1)

    # Else, solve the general problem using Dynamic Programming.

    forced = _iup_contour_bound_forced_set(deltas, coords, tolerance)
    # The _iup_contour_optimize_dp() routine returns the optimal encoding
    # solution given the constraint that the last point is always encoded.
    # To remove this constraint, we use two different methods, depending on
    # whether forced set is non-empty or not:

    # Debugging: Make the next if always take the second branch and observe
    # if the font size changes (reduced); that would mean the forced-set
    # has members it should not have.
    if forced:
        # Forced set is non-empty: rotate the contour start point
        # such that the last point in the list is a forced point.
        k = (n - 1) - max(forced)
        assert k >= 0

        deltas = _rot_list(deltas, k)
        coords = _rot_list(coords, k)
        forced = _rot_set(forced, k, n)

        # Debugging: Pass a set() instead of forced variable to the next call
        # to exercise forced-set computation for under-counting.
        chain, costs = _iup_contour_optimize_dp(deltas, coords, forced, tolerance)

        # Assemble solution.
        solution = set()
        i = n - 1
        while i is not None:
            solution.add(i)
            i = chain[i]
        solution.remove(-1)

        # if not forced <= solution:
        # 	print("coord", coords)
        # 	print("deltas", deltas)
        # 	print("len", len(deltas))
        assert forced <= solution, (forced, solution)

        deltas = [deltas[i] if i in solution else None for i in range(n)]

        deltas = _rot_list(deltas, -k)
    else:
        # Repeat the contour an extra time, solve the new case, then look for solutions of the
        # circular n-length problem in the solution for new linear case.  I cannot prove that
        # this always produces the optimal solution...
        chain, costs = _iup_contour_optimize_dp(
            deltas + deltas, coords + coords, forced, tolerance, n
        )
        best_sol, best_cost = None, n + 1

        for start in range(n - 1, len(costs) - 1):
            # Assemble solution.
            solution = set()
            i = start
            while i > start - n:
                solution.add(i % n)
                i = chain[i]
            if i == start - n:
                cost = costs[start] - costs[start - n]
                if cost <= best_cost:
                    best_sol, best_cost = solution, cost

        # if not forced <= best_sol:
        # 	print("coord", coords)
        # 	print("deltas", deltas)
        # 	print("len", len(deltas))
        assert forced <= best_sol, (forced, best_sol)

        deltas = [deltas[i] if i in best_sol else None for i in range(n)]

    return deltas

