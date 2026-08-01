
def test_fcode_Piecewise():
    x = symbols('x')
    expr = Piecewise((x, x < 1), (x**2, True))
    # Check that inline conditional (merge) fails if standard isn't 95+
    raises(NotImplementedError, lambda: fcode(expr))
    code = fcode(expr, standard=95)
    expected = "      merge(x, x**2, x < 1)"
    assert code == expected
    assert fcode(Piecewise((x, x < 1), (x**2, True)), assign_to="var") == (
        "      if (x < 1) then\n"
        "         var = x\n"
        "      else\n"
        "         var = x**2\n"
        "      end if"
    )
    a = cos(x)/x
    b = sin(x)/x
    for i in range(10):
        a = diff(a, x)
        b = diff(b, x)
    expected = (
        "      if (x < 0) then\n"
        "         weird_name = -cos(x)/x + 10*sin(x)/x**2 + 90*cos(x)/x**3 - 720*\n"
        "     @ sin(x)/x**4 - 5040*cos(x)/x**5 + 30240*sin(x)/x**6 + 151200*cos(x\n"
        "     @ )/x**7 - 604800*sin(x)/x**8 - 1814400*cos(x)/x**9 + 3628800*sin(x\n"
        "     @ )/x**10 + 3628800*cos(x)/x**11\n"
        "      else\n"
        "         weird_name = -sin(x)/x - 10*cos(x)/x**2 + 90*sin(x)/x**3 + 720*\n"
        "     @ cos(x)/x**4 - 5040*sin(x)/x**5 - 30240*cos(x)/x**6 + 151200*sin(x\n"
        "     @ )/x**7 + 604800*cos(x)/x**8 - 1814400*sin(x)/x**9 - 3628800*cos(x\n"
        "     @ )/x**10 + 3628800*sin(x)/x**11\n"
        "      end if"
    )
    code = fcode(Piecewise((a, x < 0), (b, True)), assign_to="weird_name")
    assert code == expected
    code = fcode(Piecewise((x, x < 1), (x**2, x > 1), (sin(x), True)), standard=95)
    expected = "      merge(x, merge(x**2, sin(x), x > 1), x < 1)"
    assert code == expected
    # Check that Piecewise without a True (default) condition error
    expr = Piecewise((x, x < 1), (x**2, x > 1), (sin(x), x > 0))
    raises(ValueError, lambda: fcode(expr))

