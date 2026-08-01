
def _dup_left_decompose(f, h, K):
    """Helper function for :func:`_dup_decompose`."""
    g, i = {}, 0

    while f:
        q, r = dup_div(f, h, K)

        if dup_degree(r) > 0:
            return None
        else:
            g[i] = dup_LC(r, K)
            f, i = q, i + 1

    return dup_from_raw_dict(g, K)

