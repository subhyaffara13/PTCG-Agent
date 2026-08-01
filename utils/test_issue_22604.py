
def test_issue_22604():
    x1, x2 = symbols('x1, x2', cls = Function)
    t, k1, k2, m1, m2 = symbols('t k1 k2 m1 m2', real = True)
    k1, k2, m1, m2 = 1, 1, 1, 1
    eq1 = Eq(m1*diff(x1(t), t, 2) + k1*x1(t) - k2*(x2(t) - x1(t)), 0)
    eq2 = Eq(m2*diff(x2(t), t, 2) + k2*(x2(t) - x1(t)), 0)
    eqs = [eq1, eq2]
    [x1sol, x2sol] = dsolve(eqs, [x1(t), x2(t)], ics = {x1(0):0, x1(t).diff().subs(t,0):0, \
                                                        x2(0):1, x2(t).diff().subs(t,0):0})
    assert x1sol == Eq(x1(t), sqrt(3 - sqrt(5))*(sqrt(10) + 5*sqrt(2))*cos(sqrt(2)*t*sqrt(3 - sqrt(5))/2)/20 + \
                       (-5*sqrt(2) + sqrt(10))*sqrt(sqrt(5) + 3)*cos(sqrt(2)*t*sqrt(sqrt(5) + 3)/2)/20)
    assert x2sol == Eq(x2(t), (sqrt(5) + 5)*cos(sqrt(2)*t*sqrt(3 - sqrt(5))/2)/10 + (5 - sqrt(5))*cos(sqrt(2)*t*sqrt(sqrt(5) + 3)/2)/10)

