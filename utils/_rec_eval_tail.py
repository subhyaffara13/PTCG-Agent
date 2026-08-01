
def _rec_eval_tail(g, i, A, u, K):
    """Recursive helper for :func:`dmp_eval_tail`."""
    if i == u:
        return dup_eval(g, A[-1], K)
    else:
        h = [ _rec_eval_tail(c, i + 1, A, u, K) for c in g ]

        if i < u - len(A) + 1:
            return h
        else:
            return dup_eval(h, A[-u + i - 1], K)

