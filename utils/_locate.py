
def _locate(x, y, w, h, summed_widths, equal_heights, fig_w, fig_h, anchor):

    total_width = fig_w * w
    max_height = fig_h * h

    # Determine the k factors.
    n = len(equal_heights)
    eq_rels, eq_abss = equal_heights.T
    sm_rels, sm_abss = summed_widths.T
    A = np.diag([*eq_rels, 0])
    A[:n, -1] = -1
    A[-1, :-1] = sm_rels
    B = [*(-eq_abss), total_width - sm_abss.sum()]
    # A @ K = B: This finds factors {k_0, ..., k_{N-1}, H} so that
    #   eq_rel_i * k_i + eq_abs_i = H for all i: all axes have the same height
    #   sum(sm_rel_i * k_i + sm_abs_i) = total_width: fixed total width
    # (foo_rel_i * k_i + foo_abs_i will end up being the size of foo.)
    *karray, height = np.linalg.solve(A, B)
    if height > max_height:  # Additionally, upper-bound the height.
        karray = (max_height - eq_abss) / eq_rels

    # Compute the offsets corresponding to these factors.
    ox = np.cumsum([0, *(sm_rels * karray + sm_abss)])
    ww = (ox[-1] - ox[0]) / fig_w
    h0_rel, h0_abs = equal_heights[0]
    hh = (karray[0]*h0_rel + h0_abs) / fig_h
    pb = mtransforms.Bbox.from_bounds(x, y, w, h)
    pb1 = mtransforms.Bbox.from_bounds(x, y, ww, hh)
    x0, y0 = pb1.anchored(anchor, pb).p0

    return x0, y0, ox, hh

