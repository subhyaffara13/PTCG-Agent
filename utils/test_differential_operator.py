
def test_differential_operator():
    x = Symbol('x')
    f = Function('f')
    d = DifferentialOperator(Derivative(f(x), x), f(x))
    g = Wavefunction(x**2, x)
    assert qapply(d*g) == Wavefunction(2*x, x)
    assert d.expr == Derivative(f(x), x)
    assert d.function == f(x)
    assert d.variables == (x,)
    assert diff(d, x) == DifferentialOperator(Derivative(f(x), x, 2), f(x))

    d = DifferentialOperator(Derivative(f(x), x, 2), f(x))
    g = Wavefunction(x**3, x)
    assert qapply(d*g) == Wavefunction(6*x, x)
    assert d.expr == Derivative(f(x), x, 2)
    assert d.function == f(x)
    assert d.variables == (x,)
    assert diff(d, x) == DifferentialOperator(Derivative(f(x), x, 3), f(x))

    d = DifferentialOperator(1/x*Derivative(f(x), x), f(x))
    assert d.expr == 1/x*Derivative(f(x), x)
    assert d.function == f(x)
    assert d.variables == (x,)
    assert diff(d, x) == \
        DifferentialOperator(Derivative(1/x*Derivative(f(x), x), x), f(x))
    assert qapply(d*g) == Wavefunction(3*x, x)

    # 2D cartesian Laplacian
    y = Symbol('y')
    d = DifferentialOperator(Derivative(f(x, y), x, 2) +
                             Derivative(f(x, y), y, 2), f(x, y))
    w = Wavefunction(x**3*y**2 + y**3*x**2, x, y)
    assert d.expr == Derivative(f(x, y), x, 2) + Derivative(f(x, y), y, 2)
    assert d.function == f(x, y)
    assert d.variables == (x, y)
    assert diff(d, x) == \
        DifferentialOperator(Derivative(d.expr, x), f(x, y))
    assert diff(d, y) == \
        DifferentialOperator(Derivative(d.expr, y), f(x, y))
    assert qapply(d*w) == Wavefunction(2*x**3 + 6*x*y**2 + 6*x**2*y + 2*y**3,
                                       x, y)

    # 2D polar Laplacian (th = theta)
    r, th = symbols('r th')
    d = DifferentialOperator(1/r*Derivative(r*Derivative(f(r, th), r), r) +
                             1/(r**2)*Derivative(f(r, th), th, 2), f(r, th))
    w = Wavefunction(r**2*sin(th), r, (th, 0, pi))
    assert d.expr == \
        1/r*Derivative(r*Derivative(f(r, th), r), r) + \
        1/(r**2)*Derivative(f(r, th), th, 2)
    assert d.function == f(r, th)
    assert d.variables == (r, th)
    assert diff(d, r) == \
        DifferentialOperator(Derivative(d.expr, r), f(r, th))
    assert diff(d, th) == \
        DifferentialOperator(Derivative(d.expr, th), f(r, th))
    assert qapply(d*w) == Wavefunction(3*sin(th), r, (th, 0, pi))

