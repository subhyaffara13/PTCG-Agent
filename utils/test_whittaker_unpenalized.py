
def test_whittaker_unpenalized():
    """Test whittaker for lamb=0."""
    n = 10
    y = np.sin(2*np.pi * np.linspace(0, 1, n))
    wh = whittaker_henderson(y, lamb=0)
    assert_allclose(wh.x, y, rtol=1e-11)
    assert not np.may_share_memory(wh.x, y)

