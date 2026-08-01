
def test_sympy__physics__control__lti__Series():
    from sympy.physics.control import Series, TransferFunction
    tf1 = TransferFunction(x**2 - y**3, y - z, x)
    tf2 = TransferFunction(y - x, z + y, x)
    assert _test_args(Series(tf1, tf2))

