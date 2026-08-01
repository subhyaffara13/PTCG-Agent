
def test_whittaker_limit_zero_penalty(order):
    """Test whittaker for penalty lamb close to zero."""
    rng = np.random.default_rng(42)
    n = 100
    y = np.sin(2*np.pi * np.linspace(0, 1, n))
    noise = rng.standard_normal(n)
    signal = y + noise

    # In the limit of a zero penalty, the smoothing results in reproducing the signal.
    wh = whittaker_henderson(signal, lamb=1e-7, order=order)
    assert_allclose(wh.x, signal, rtol=1e-4, atol=1e-5)
    assert wh.lamb == 1e-7

