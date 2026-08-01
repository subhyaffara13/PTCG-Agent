
def test_python_div_zero_issue_11306():
    if not numpy:
        skip("numpy not installed.")
    p = Piecewise((1 / x, y < -1), (x, y < 1), (1 / x, True))
    f = lambdify([x, y], p, modules='numpy')
    with numpy.errstate(divide='ignore'):
        assert float(f(numpy.array(0), numpy.array(0.5))) == 0
        assert float(f(numpy.array(0), numpy.array(1))) == float('inf')

