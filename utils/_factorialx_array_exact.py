
def _factorialx_array_exact(n, k=1):
    """
    Exact computation of factorial for an array.

    The factorials are computed in incremental fashion, by taking
    the sorted unique values of n and multiplying the intervening
    numbers between the different unique values.

    In other words, the factorial for the largest input is only
    computed once, with each other result computed in the process.

    k > 1 corresponds to the multifactorial.
    """
    un = np.unique(n)

    # Convert to object array if np.int64 can't handle size
    if k in _FACTORIALK_LIMITS_64BITS.keys():
        if un[-1] > _FACTORIALK_LIMITS_64BITS[k]:
            # e.g. k=1: 21! > np.iinfo(np.int64).max
            dt = object
        elif un[-1] > _FACTORIALK_LIMITS_32BITS[k]:
            # e.g. k=3: 26!!! > np.iinfo(np.int32).max
            dt = np.int64
        else:
            dt = np.dtype("long")
    else:
        # for k >= 10, we always use object
        dt = object

    out = np.empty_like(n, dtype=dt)

    # Handle invalid/trivial values
    un = un[un > 1]
    out[n < 2] = 1
    out[n < 0] = 0

    # Calculate products of each range of numbers
    # we can only multiply incrementally if the values are k apart;
    # therefore we partition `un` into "lanes", i.e. its residues modulo k
    for lane in range(0, k):
        ul = un[(un % k) == lane] if k > 1 else un
        if ul.size:
            # after np.unique, un resp. ul are sorted, ul[0] is the smallest;
            # cast to python ints to avoid overflow with np.int-types
            val = _range_prod(1, int(ul[0]), k=k)
            out[n == ul[0]] = val
            for i in range(len(ul) - 1):
                # by the filtering above, we have ensured that prev & current
                # are a multiple of k apart
                prev = ul[i]
                current = ul[i + 1]
                # we already multiplied all factors until prev; continue
                # building the full factorial from the following (`prev + 1`);
                # use int() for the same reason as above
                val *= _range_prod(int(prev + 1), int(current), k=k)
                out[n == current] = val

    return out

