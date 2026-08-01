
def test_whittaker_weights():
    """Test that whittaker with weights of 1 is same as without weights."""
    rng = np.random.default_rng(42)
    n = 100
    y = np.sin(2*np.pi * np.linspace(0, 1, n))
    noise = rng.standard_normal(n)
    signal = y + noise
    wh1 = whittaker_henderson(signal, lamb=1)
    w = np.ones_like(signal)
    wh2 = whittaker_henderson(signal, lamb=1, weights=w)
    assert_allclose(wh1.x, wh2.x, rtol=1e-11)

    # Multiplying penalty and weights by the same number does not change the result.
    wh3 = whittaker_henderson(signal, lamb=3, weights=3*w)
    assert_allclose(wh3.x, wh1.x, rtol=1e-11)

