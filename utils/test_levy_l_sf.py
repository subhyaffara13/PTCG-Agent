
def test_levy_l_sf():
    # Test levy_l.sf for small arguments.
    x = np.array([-0.016, -0.01, -0.005, -0.0015])
    # Expected values were calculated with mpmath.
    expected = np.array([2.6644463892359302e-15,
                         1.523970604832107e-23,
                         2.0884875837625492e-45,
                         5.302850374626878e-147])
    y = stats.levy_l.sf(x)
    assert_allclose(y, expected, rtol=1e-13)

