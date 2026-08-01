
def test_rs_series_ConstantInExpr():
    x, a = symbols('x a')
    assert rs_series(log(1 + x), x, 5).as_expr() == -x**4/4 + x**3/3 - \
            x**2/2 + x
    assert rs_series(log(1 + 4*x), x, 5).as_expr() == -64*x**4 + 64*x**3/3 - \
            8*x**2 + 4*x
    assert rs_series(log(1 + x + x**2), x, 10).as_expr() == -2*x**9/9 + \
            x**8/8 + x**7/7 - x**6/3 + x**5/5 + x**4/4 - 2*x**3/3 + x**2/2 + x
    assert rs_series(log(1 + x*a**2), x, 7).as_expr() == -x**6*a**12/6 + \
            x**5*a**10/5 - x**4*a**8/4 + x**3*a**6/3 - x**2*a**4/2 + x*a**2

    assert rs_series(atan(1 + x), x, 9).as_expr() == -x**7/112 + x**6/48 - x**5/40 \
            + x**3/12 - x**2/4 + x/2 + pi/4
    assert rs_series(atan(1 + x + x**2),x, 9).as_expr() == -15*x**7/112 - x**6/48 + \
            9*x**5/40 - 5*x**3/12 + x**2/4 + x/2 + pi/4
    assert rs_series(atan(1 + x * a), x, 9).as_expr() == -a**7*x**7/112 + a**6*x**6/48 \
            - a**5*x**5/40 + a**3*x**3/12 - a**2*x**2/4 + a*x/2 + pi/4

    assert rs_series(tanh(1 + x), x, 5).as_expr() == -5*x**4*tanh(1)**3/3 + x**4* \
            tanh(1)**5 + 2*x**4*tanh(1)/3 - x**3*tanh(1)**4 - x**3/3 + 4*x**3*tanh(1) \
           **2/3 - x**2*tanh(1) + x**2*tanh(1)**3 - x*tanh(1)**2 + x + tanh(1)
    assert rs_series(tanh(1 + x * a), x, 3).as_expr() == -a**2*x**2*tanh(1) + a**2*x** \
            2*tanh(1)**3 - a*x*tanh(1)**2 + a*x + tanh(1)

    assert rs_series(sinh(1 + x), x, 5).as_expr() == x**4*sinh(1)/24 + x**3*cosh(1)/6 + \
            x**2*sinh(1)/2 + x*cosh(1) + sinh(1)
    assert rs_series(sinh(1 + x * a), x, 5).as_expr() == a**4*x**4*sinh(1)/24 + \
            a**3*x**3*cosh(1)/6 + a**2*x**2*sinh(1)/2 + a*x*cosh(1) + sinh(1)

    assert rs_series(cosh(1 + x), x, 5).as_expr() == x**4*cosh(1)/24 + x**3*sinh(1)/6 + \
            x**2*cosh(1)/2 + x*sinh(1) + cosh(1)
    assert rs_series(cosh(1 + x * a), x, 5).as_expr() == a**4*x**4*cosh(1)/24 + \
            a**3*x**3*sinh(1)/6 + a**2*x**2*cosh(1)/2 + a*x*sinh(1) + cosh(1)

