
def fpcheck(x, t, k, periodic=False):
    """Check consistency of data vector `x` and knot vector `t`.

    Parameters
    ----------
    x : array_like, shape (m,)
        1D sorted array of data points.
    t : array_like, shape (n,)
        1D non-decreasing knot vector.
    k : int
        Degree of the spline.
    periodic : bool, optional
        Whether the spline is periodic. Default is False.

    Raises
    ------
    ValueError
        If the configuration of `x`, `t`, and `k` violates any required condition.
    """
    # This routine is a unified clone of the FITPACK Fortran routines `fpchec.f`
    # and `fpchep.f`:
    # - https://github.com/scipy/scipy/blob/main/scipy/interpolate/fitpack/fpchec.f
    # - https://github.com/scipy/scipy/blob/main/scipy/interpolate/fitpack/fpchep.f
    #
    # These routines verify the number and position of the knots t(j), j=1,...,n,
    # of a spline of degree k, relative to the number and distribution of data points
    # x(i), i=1,...,m. If all of the following conditions are fulfilled,
    # validation passes.
    #
    # For non-periodic splines:
    #   1) k+1 <= n-k-1 <= m
    #   2) t(1) <= t(2) <= ... <= t(k+1)
    #      t(n-k) <= t(n-k+1) <= ... <= t(n)
    #   3) t(k+1) < t(k+2) < ... < t(n-k)
    #   4) t(k+1) <= x(i) <= t(n-k)
    #   5) Schoenberg-Whitney conditions hold: there exists a subset y(j) such that
    #        t(j) < y(j) < t(j+k+1), for j = 1, ..., n-k-1
    #
    # For periodic splines:
    #   1) k+1 <= n-k-1 <= m + k - 1
    #   2) Same boundary knot monotonicity as above
    #   3) Same strict interior knot increase as above
    #   4) t(k+1) <= x(i) <= t(n-k)
    #   5) Schoenberg-Whitney conditions must hold for *some periodic shift*
    #        of the data sequence; i.e. wrapped data points x(i) must satisfy
    #        t(j) < y(j) < t(j+k+1), j = k+1, ..., n-k-1
    x = np.asarray(x)
    t = np.asarray(t)

    if x.ndim != 1 or t.ndim != 1:
        raise ValueError(f"Expect `x` and `t` be 1D sequences. Got {x = } and {t = }")

    m = x.shape[0]
    n = t.shape[0]
    nk1 = n - k - 1

    # check condition no 1
    if periodic:
        # c      1) k+1 <= nk1 <= m+k-1
        if not (k + 1 <= nk1 <= m + k - 1):
            raise ValueError(f"Need k+1 <= n-k-1 <= m+k-1. Got {m = }, {n = }, {k = }")
    else:
        # c      1) k+1 <= n-k-1 <= m
        if not (k + 1 <= nk1 <= m):
            raise ValueError(f"Need k+1 <= n-k-1 <= m. Got {m = }, {n = } and {k = }.")

    # check condition no 2
    # c      2) t(1) <= t(2) <= ... <= t(k+1)
    # c         t(n-k) <= t(n-k+1) <= ... <= t(n)
    if (t[:k+1] > t[1:k+2]).any():
        raise ValueError(f"First k knots must be ordered; got {t = }.")

    if (t[nk1:] < t[nk1-1:-1]).any():
        raise ValueError(f"Last k knots must be ordered; got {t = }.")

    # c  check condition no 3
    # c      3) t(k+1) < t(k+2) < ... < t(n-k)
    if (t[k+1:n-k] <= t[k:n-k-1]).any():
        raise ValueError(f"Internal knots must be distinct. Got {t = }.")

    # c  check condition no 4
    # c      4) t(k+1) <= x(i) <= t(n-k)
    # NB: FITPACK's fpchec only checks x[0] & x[-1], so we follow.
    if (x[0] < t[k]) or (x[-1] > t[n-k-1]):
        raise ValueError(f"Out of bounds: {x = } and {t = }.")

    # c  check condition no 5
    # c      5) the conditions specified by Schoenberg and Whitney must hold
    # c         for at least one subset of data points y(j) such that
    # c             t(j) < y(j) < t(j+k+1)
    # c
    # c         For non-periodic splines:
    # c             j = 1, 2, ..., n-k-1 (i.e., j in [1, n-k-1])
    # c             The data points must lie strictly inside some B-spline supports.
    # c
    # c         For periodic splines:
    # c             j = k+1, ..., n-k-1
    # c             The condition must hold for a wrapped subset of the data points,
    # c             i.e., there exists a cyclic shift of the data such that
    # c                 t(j) < x(i) < t(j+k+1)
    # c             holds for all j in that range. The test must account for the
    # c             periodic domain length: per = t(n-k) - t(k+1), and wrap around x(i)
    # c             as x(i) + per if needed.
    mesg = f"Schoenberg-Whitney condition is violated with {t = } and {x =}."

    if periodic:
        per = t[n - k - 1] - t[k]
        m1 = m - 1
        for shift in range(1, m):
            for j in range(k, nk1):
                tj = t[j]
                tl = t[j + k + 1]
                found = False
                for i in range(shift, shift + m1 + 1):
                    idx = i if i < m else i - m
                    xi = x[idx] + (0 if i < m else per)
                    if tj < xi < tl:
                        found = True
                        break
                if not found:
                    break
            else:
                return
        raise ValueError(mesg)
    else:
        if (x[0] >= t[k+1]) or (x[-1] <= t[n-k-2]):
            raise ValueError(mesg)

        m = x.shape[0]
        l = k+1
        nk3 = n - k - 3
        if nk3 < 2:
            return
        for j in range(1, nk3+1):
            tj = t[j]
            l += 1
            tl = t[l]
            i = np.argmax(x > tj)
            if i >= m-1:
                raise ValueError(mesg)
            if x[i] >= tl:
                raise ValueError(mesg)
        return

