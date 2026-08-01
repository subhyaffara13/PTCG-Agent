
def test_cosm1_apart():
    x = Symbol('x')

    expr1 = 1/cos(x) - 1
    opt1 = optimize(expr1, [cosm1_opt])
    assert opt1 == -cosm1(x)/cos(x)
    if scipy:
        _check_num_lambdify(expr1, opt1, {x: S(10)**-30}, 5e-61, lambdify_kw={"modules": 'scipy'})

    expr2 = 2/cos(x) - 2
    opt2 = optimize(expr2, optims_scipy)
    assert opt2 == -2*cosm1(x)/cos(x)
    if scipy:
        _check_num_lambdify(expr2, opt2, {x: S(10)**-30}, 1e-60, lambdify_kw={"modules": 'scipy'})

    expr3 = pi/cos(3*x) - pi
    opt3 = optimize(expr3, [cosm1_opt])
    assert opt3 == -pi*cosm1(3*x)/cos(3*x)
    if scipy:
        _check_num_lambdify(expr3, opt3, {x: S(10)**-30/3}, float(5e-61*pi), lambdify_kw={"modules": 'scipy'})

