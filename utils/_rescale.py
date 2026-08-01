
def _rescale(
    betweenness, n, *, normalized, directed, endpoints=True, sampled_nodes=None
):
    # For edge betweenness, `endpoints` is always `True`.

    k = None if sampled_nodes is None else len(sampled_nodes)
    # N is used to count the number of valid (s, t) pairs where s != t that
    # could have a path pass through v. If endpoints is False, then v must
    # not be the target t, hence why we subtract by 1.
    N = n if endpoints else n - 1
    if N < 2:
        # No rescaling necessary: b=0 for all nodes
        return betweenness

    K_source = N if k is None else k

    if k is None or endpoints:
        # No sampling adjustment needed
        if normalized:
            # Divide by the number of valid (s, t) node pairs that could have
            # a path through v where s != t.
            scale = 1 / (K_source * (N - 1))
        else:
            # Scale to the full BC
            if not directed:
                # The non-normalized BC values are computed the same way for
                # directed and undirected graphs: shortest paths are computed and
                # counted for each *ordered* (s, t) pair. Undirected graphs should
                # only count valid *unordered* node pairs {s, t}; that is, (s, t)
                # and (t, s) should be counted only once. We correct for this here.
                correction = 2
            else:
                correction = 1
            scale = N / (K_source * correction)

        if scale != 1:
            for v in betweenness:
                betweenness[v] *= scale
        return betweenness

    # Sampling adjustment needed when excluding endpoints when using k. In this
    # case, we need to handle source nodes differently from non-source nodes,
    # because source nodes can't include themselves since endpoints are excluded.
    # Without this, k == n would be a special case that would violate the
    # assumption that node `v` is not one of the (s, t) node pairs.
    if normalized:
        # NaN for undefined 0/0; there is no data for source node when k=1
        scale_source = 1 / ((K_source - 1) * (N - 1)) if K_source > 1 else math.nan
        scale_nonsource = 1 / (K_source * (N - 1))
    else:
        correction = 1 if directed else 2
        scale_source = N / ((K_source - 1) * correction) if K_source > 1 else math.nan
        scale_nonsource = N / (K_source * correction)

    sampled_nodes = set(sampled_nodes)
    for v in betweenness:
        betweenness[v] *= scale_source if v in sampled_nodes else scale_nonsource
    return betweenness

