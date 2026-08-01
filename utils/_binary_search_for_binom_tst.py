
def _binary_search_for_binom_tst(a, d, lo, hi, *, xp):
    """
    Conducts an implicit binary search on a function specified by `a`.

    Meant to be used on the binomial PMF for the case of two-sided tests
    to obtain the value on the other side of the mode where the tail
    probability should be computed. The values on either side of
    the mode are always in order, meaning binary search is applicable.

    Parameters
    ----------
    a : callable
      The function over which to perform binary search. Its values
      for inputs lo and hi should be in ascending order.
    d : float
      The value to search.
    lo : int
      The lower end of range to search.
    hi : int
      The higher end of the range to search.

    Returns
    -------
    int
      The index, i between lo and hi
      such that a(i)<=d<a(i+1)
    """
    d = xp.asarray(d, copy=True)
    lo = xp.asarray(lo, copy=True)
    hi = xp.asarray(hi, copy=True)
    while xp.any(lo < hi):
        mid = lo + (hi-lo)//2
        midval = a(mid)

        i_lt = midval < d
        lo = xpx.at(lo)[i_lt].set(mid[i_lt] + 1)

        i_gt = midval > d
        hi = xpx.at(hi)[i_gt].set(mid[i_gt] - 1)

        i_eq = (midval == d)
        mid_i_eq = mid[i_eq]
        lo = xpx.at(lo)[i_eq].set(mid_i_eq)
        hi = xpx.at(hi)[i_eq].set(mid_i_eq)

    return xp.where(a(lo) <= d, lo, lo-1)

