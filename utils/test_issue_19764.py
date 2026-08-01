
def test_issue_19764():
    if not numpy:
        skip("numpy not installed")

    expr = Array([x, x**2])
    f = lambdify(x, expr, 'numpy')

    assert f(1).__class__ == numpy.ndarray

