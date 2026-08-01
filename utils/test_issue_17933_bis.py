
def test_issue_17933_bis():
    # nonlinsolve's result depends on the 'default_sort_key' ordering of
    # the unknowns.
    eq1 = x*sin(45) - y*cos(q)
    eq2 = x*cos(45) - y*sin(q)
    eq3 = 9*x*sin(45)/10 + y*cos(q)
    eq4 = 9*x*cos(45)/10 + y*sin(z) - z
    zz = Symbol('zz')
    eqs = [e.subs(q, zz) for e in (eq1, eq2, eq3, eq4)]
    assert nonlinsolve(eqs, x, y, z, zz) == FiniteSet((0, 0, 0, zz))

