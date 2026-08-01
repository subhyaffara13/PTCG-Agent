
def test_vector_discontinuous():
    f = lambdify(x, (-1/x, 1/x))
    raises(ZeroDivisionError, lambda: f(0))
    assert f(1) == (-1.0, 1.0)
    assert f(2) == (-0.5, 0.5)
    assert f(-2) == (0.5, -0.5)

