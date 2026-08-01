
def _get_pairs(k, h0, inclusive, dtype, xp, work):
    # Retrieve the specified abscissa-weight pairs from the cache
    # If `inclusive`, return all up to and including the specified level
    if (len(work.pair_cache.indices) <= k+2
        or not isinstance (h0, type(work.pair_cache.h0))
        or h0 != work.pair_cache.h0):
            _pair_cache(k, h0, xp, work)

    xjc = work.pair_cache.xjc
    wj = work.pair_cache.wj
    indices = work.pair_cache.indices

    start = 0 if inclusive else indices[k]
    end = indices[k+1]

    return xp.astype(xjc[start:end], dtype), xp.astype(wj[start:end], dtype)

