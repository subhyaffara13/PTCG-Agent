
def test_tbound_respected_larger_interval(method):
    """Regression test for gh-8848"""
    def V(r):
        return -11/r + 10 * r / (0.05 + r**2)

    def func(t, p):
        if t < -17 or t > 2:
            raise ValueError("Function was evaluated outside interval")
        P = p[0]
        Q = p[1]
        r = np.exp(t)
        dPdr = r * Q
        dQdr = -2.0 * r * ((-0.2 - V(r)) * P + 1 / r * Q)
        return np.array([dPdr, dQdr])

    result = solve_ivp(func,
                       (-17, 2),
                       y0=np.array([1, -11]),
                       max_step=0.03,
                       vectorized=False,
                       t_eval=None,
                       atol=1e-8,
                       rtol=1e-5)
    assert result.success

