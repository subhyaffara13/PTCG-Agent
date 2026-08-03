import math


def test_gh_21661(xp, n):
    one = xp.asarray(1.0)
    mu = 0.0
    r = np.logspace(-7, 1, n)
    dln = math.log(r[1] / r[0])
    offset = fhtoffset(dln, initial=-6 * np.log(10), mu=mu)
    r = xp.asarray(r, dtype=one.dtype)
    k = math.exp(offset) / xp.flip(r, axis=-1)

    def f(x, mu):
        return x**(mu + 1)*xp.exp(-x**2/2)

    a_r = f(r, mu)
    fht_val = fht(a_r, dln, mu=mu, offset=offset)
    a_k = f(k, mu)
    rel_err = xp.max(xp.abs((fht_val - a_k) / a_k))
    xp_assert_less(rel_err, xp.asarray(7.28e+16)[()])

