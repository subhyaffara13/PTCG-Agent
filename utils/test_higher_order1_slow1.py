
def test_higher_order1_slow1():
    x, y = symbols("x y", cls=Function)
    t = symbols("t")

    eq = [
        Eq(diff(x(t),t,t), (log(t)+t**2)*diff(x(t),t)+(log(t)+t**2)*3*diff(y(t),t)),
        Eq(diff(y(t),t,t), (log(t)+t**2)*2*diff(x(t),t)+(log(t)+t**2)*9*diff(y(t),t))
    ]
    sol, = dsolve_system(eq, simplify=False, doit=False)
    # The solution is too long to write out explicitly and checkodesol is too
    # slow so we test for particular values of t:
    for e in eq:
        res = (e.lhs - e.rhs).subs({sol[0].lhs:sol[0].rhs, sol[1].lhs:sol[1].rhs})
        res = res.subs({d: d.doit(deep=False) for d in res.atoms(Derivative)})
        assert ratsimp(res.subs(t, 1)) == 0

