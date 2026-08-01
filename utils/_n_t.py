
def _nT(n, k):
    """Return the partitions of ``n`` items into ``k`` parts. This
    is used by ``nT`` for the case when ``n`` is an integer."""
    # really quick exits
    if k > n or k < 0:
        return 0
    if k in (1, n):
        return 1
    if k == 0:
        return 0
    # exits that could be done below but this is quicker
    if k == 2:
        return n//2
    d = n - k
    if d <= 3:
        return d
    # quick exit
    if 3*k >= n:  # or, equivalently, 2*k >= d
        # all the information needed in this case
        # will be in the cache needed to calculate
        # partition(d), so...
        # update cache
        tot = _partition_rec(d)
        # and correct for values not needed
        if d - k > 0:
            tot -= sum(_partition_rec.fetch_item(slice(d - k)))
        return tot
    # regular exit
    # nT(n, k) = Sum(nT(n - k, m), (m, 1, k));
    # calculate needed nT(i, j) values
    p = [1]*d
    for i in range(2, k + 1):
        for m  in range(i + 1, d):
            p[m] += p[m - i]
        d -= 1
    # if p[0] were appended to the end of p then the last
    # k values of p are the nT(n, j) values for 0 < j < k in reverse
    # order p[-1] = nT(n, 1), p[-2] = nT(n, 2), etc.... Instead of
    # putting the 1 from p[0] there, however, it is simply added to
    # the sum below which is valid for 1 < k <= n//2
    return (1 + sum(p[1 - k:]))

