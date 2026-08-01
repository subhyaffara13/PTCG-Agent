
def test_subs_in_derivative():
    expr = sin(x*exp(y))
    u = Function('u')
    v = Function('v')
    assert Derivative(expr, y).subs(expr, y) == Derivative(y, y)
    assert Derivative(expr, y).subs(y, x).doit() == \
        Derivative(expr, y).doit().subs(y, x)
    assert Derivative(f(x, y), y).subs(y, x) == Subs(Derivative(f(x, y), y), y, x)
    assert Derivative(f(x, y), y).subs(x, y) == Subs(Derivative(f(x, y), y), x, y)
    assert Derivative(f(x, y), y).subs(y, g(x, y)) == Subs(Derivative(f(x, y), y), y, g(x, y)).doit()
    assert Derivative(f(x, y), y).subs(x, g(x, y)) == Subs(Derivative(f(x, y), y), x, g(x, y))
    assert Derivative(f(x, y), g(y)).subs(x, g(x, y)) == Derivative(f(g(x, y), y), g(y))
    assert Derivative(f(u(x), h(y)), h(y)).subs(h(y), g(x, y)) == \
        Subs(Derivative(f(u(x), h(y)), h(y)), h(y), g(x, y)).doit()
    assert Derivative(f(x, y), y).subs(y, z) == Derivative(f(x, z), z)
    assert Derivative(f(x, y), y).subs(y, g(y)) == Derivative(f(x, g(y)), g(y))
    assert Derivative(f(g(x), h(y)), h(y)).subs(h(y), u(y)) == \
        Derivative(f(g(x), u(y)), u(y))
    assert Derivative(f(x, f(x, x)), f(x, x)).subs(
        f, Lambda((x, y), x + y)) == Subs(
        Derivative(z + x, z), z, 2*x)
    assert Subs(Derivative(f(f(x)), x), f, cos).doit() == sin(x)*sin(cos(x))
    assert Subs(Derivative(f(f(x)), f(x)), f, cos).doit() == -sin(cos(x))
    # Issue 13791. No comparison (it's a long formula) but this used to raise an exception.
    assert isinstance(v(x, y, u(x, y)).diff(y).diff(x).diff(y), Expr)
    # This is also related to issues 13791 and 13795; issue 15190
    F = Lambda((x, y), exp(2*x + 3*y))
    abstract = f(x, f(x, x)).diff(x, 2)
    concrete = F(x, F(x, x)).diff(x, 2)
    assert (abstract.subs(f, F).doit() - concrete).simplify() == 0
    # don't introduce a new symbol if not necessary
    assert x in f(x).diff(x).subs(x, 0).atoms()
    # case (4)
    assert Derivative(f(x,f(x,y)), x, y).subs(x, g(y)
        ) == Subs(Derivative(f(x, f(x, y)), x, y), x, g(y))

    assert Derivative(f(x, x), x).subs(x, 0
        ) == Subs(Derivative(f(x, x), x), x, 0)
    # issue 15194
    assert Derivative(f(y, g(x)), (x, z)).subs(z, x
        ) == Derivative(f(y, g(x)), (x, x))

    df = f(x).diff(x)
    assert df.subs(df, 1) is S.One
    assert df.diff(df) is S.One
    dxy = Derivative(f(x, y), x, y)
    dyx = Derivative(f(x, y), y, x)
    assert dxy.subs(Derivative(f(x, y), y, x), 1) is S.One
    assert dxy.diff(dyx) is S.One
    assert Derivative(f(x, y), x, 2, y, 3).subs(
        dyx, g(x, y)) == Derivative(g(x, y), x, 1, y, 2)
    assert Derivative(f(x, x - y), y).subs(x, x + y) == Subs(
        Derivative(f(x, x - y), y), x, x + y)

