
def test_levy_l_isf():
    # Test roundtrip sf(isf(p)), including a small input value.
    p = np.array([3.0e-15, 0.25, 0.99])
    x = stats.levy_l.isf(p)
    q = stats.levy_l.sf(x)
    assert_allclose(q, p, rtol=5e-14)

