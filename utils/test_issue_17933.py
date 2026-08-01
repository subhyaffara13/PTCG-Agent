
def test_issue_17933():
    eq1 = x*sin(45) - y*cos(q)
    eq2 = x*cos(45) - y*sin(q)
    eq3 = 9*x*sin(45)/10 + y*cos(q)
    eq4 = 9*x*cos(45)/10 + y*sin(z) - z
    assert nonlinsolve([eq1, eq2, eq3, eq4], x, y, z, q) ==\
        FiniteSet((0, 0, 0, q))

