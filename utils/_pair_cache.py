
def _pair_cache(k, h0, xp, work):
    # Cache the abscissa-weight pairs up to a specified level.
    # Abscissae and weights of consecutive levels are concatenated.
    # `index` records the indices that correspond with each level:
    # `xjc[index[k]:index[k+1]` extracts the level `k` abscissae.
    if not isinstance(h0, type(work.pair_cache.h0)) or h0 != work.pair_cache.h0:
        work.pair_cache.xjc = xp.empty(0)
        work.pair_cache.wj = xp.empty(0)
        work.pair_cache.indices = [0]

    xjcs = [work.pair_cache.xjc]
    wjs = [work.pair_cache.wj]

    for i in range(len(work.pair_cache.indices)-1, k + 1):
        xjc, wj = _compute_pair(i, h0, xp)
        xjcs.append(xjc)
        wjs.append(wj)
        work.pair_cache.indices.append(work.pair_cache.indices[-1] + xjc.shape[0])

    work.pair_cache.xjc = xp.concat(xjcs)
    work.pair_cache.wj = xp.concat(wjs)
    work.pair_cache.h0 = h0

