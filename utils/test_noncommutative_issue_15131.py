
def test_noncommutative_issue_15131():
    x = Symbol('x', commutative=False)
    t = Symbol('t', commutative=False)
    fx = Function('Fx', commutative=False)(x)
    ft = Function('Ft', commutative=False)(t)
    A = Symbol('A', commutative=False)
    eq = fx * A * ft
    eqdt = eq.diff(t)
    assert eqdt.args[-1] == ft.diff(t)

