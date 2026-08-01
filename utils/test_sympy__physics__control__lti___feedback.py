
def test_sympy__physics__control__lti__Feedback():
    from sympy.physics.control import TransferFunction, Feedback
    tf1 = TransferFunction(x**2 - y**3, y - z, x)
    tf2 = TransferFunction(y - x, z + y, x)
    assert _test_args(Feedback(tf1, tf2))
    assert _test_args(Feedback(tf1, tf2, 1))

