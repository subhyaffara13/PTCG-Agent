
def test_custom_operator_new():
    """Using Eigen types as member variables requires a class-specific
    operator new with proper alignment"""

    o = m.CustomOperatorNew()
    np.testing.assert_allclose(o.a, 0.0)
    np.testing.assert_allclose(o.b.diagonal(), 1.0)

