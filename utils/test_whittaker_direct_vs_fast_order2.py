
def test_whittaker_direct_vs_fast_order2(n):
    """Test equivalent results"""
    rng = np.random.default_rng(42)
    signal = np.sin(2 * np.pi * np.linspace(0, 1, n)) + rng.standard_normal(n)
    x1, _ = _solve_WH_banded(signal, lamb=1.23, order=2)
    x2 = _solve_WH_order2_fast(signal, lamb=1.23)
    assert_allclose(x1, x2, rtol=1e-11)

    wh = whittaker_henderson(signal, lamb=1.23, order=2)
    assert_allclose(wh.x, x1, rtol=1e-11)

