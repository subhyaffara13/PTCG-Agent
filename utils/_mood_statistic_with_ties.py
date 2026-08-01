
def _mood_statistic_with_ties(x, y, t, m, n, N, xp):
    # First equation of "Mood's Squared Rank Test", Mielke pg 313
    E_0_T = m * (N * N - 1) / 12

    # m, n, N, t, and S are defined in the second paragraph of Mielke pg 312
    # The only difference is that our `t` has zeros interspersed with the relevant
    # numbers to keep the array rectangular, but these terms add nothing to the sum.
    S = xp.cumulative_sum(t, include_initial=True, axis=-1)
    S_i, S_i_m1 = S[..., 1:], S[..., :-1]
    # Second equation of "Mood's Squared Rank Test", Mielke pg 313
    varM = (m * n * (N + 1.0) * (N**2 - 4) / 180
            - m * n / (180 * N * (N - 1))
            * xp.sum(t * (t ** 2 - 1) * (t ** 2 - 4 + (15 * (N - S_i - S_i_m1) ** 2)),
                     axis=-1))

    # There is a formula for Phi (`phi` in code) in terms of t, S, and Psi(I) at the
    # bottom of Mielke pg 312. Psi(I) = [I - (N+1)/2]^2 is defined (with a mistake in
    # the location of the ^2) at the beginning of "Mood's Squared Rank Test" (pg 313).
    # To vectorize this calculation, let c = (N + 1) / 2, so Psi(I) = I^2 - 2*c*I + c^2.
    # We sum each of these three parts of Psi separately using formulas for sums from a
    # to b (inclusive) of terms I^2, I, and 1 where I takes on successive integers.
    def sum_I2(a, b=None):
        return (a * (a + 1) * (2 * a + 1) / 6 if b is None
                else sum_I2(b) - sum_I2(a) + a**2)

    def sum_I(a, b=None):
        return (a * (a + 1) / 2 if b is None
                else sum_I(b) - sum_I(a) + a)

    def sum_1(a, b):
        return (b - a) + 1

    with np.errstate(invalid='ignore', divide='ignore'):
        sum_I2 = sum_I2(S_i_m1 + 1, S_i)
        sum_I = sum_I(S_i_m1 + 1, S_i)
        sum_1 = sum_1(S_i_m1 + 1, S_i)
        c = (N + 1) / 2
        phi = (sum_I2 - 2*c*sum_I + sum_1*c**2) / t

    phi = xpx.at(phi)[t == 0].set(0.)  # where t = 0 we get NaNs; eliminate them

    # Mielke pg 312 defines `a` as the count of elements in sample `x` for each of the
    # unique values in the combined sample. The tricky thing is getting these to line
    # up with the locations of nonzero elements in `t`/`phi`.
    x = xp.sort(x, axis=-1)
    xy = xp.concat((x, y), axis=-1)
    i = xp.argsort(xy, stable=True, axis=-1)
    _, _, a = _stats_py._rankdata(x, method='average', return_ties=True)

    zeros = xp.zeros(a.shape[:-1] + (n,), dtype=a.dtype)
    a = xp.concat((a, zeros), axis=-1)
    a = xp.take_along_axis(a, i, axis=-1)

    # Mielke pg 312 defines test statistic `T` as the inner product `a` and `phi`
    T = xp.vecdot(a, phi, axis=-1)

    return (T - E_0_T) / xp.sqrt(varM)

