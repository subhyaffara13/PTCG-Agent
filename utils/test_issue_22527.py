
def test_issue_22527():
    t, R = symbols(r't R')
    z = Function('z')(t)
    def f(x):
        return x/sqrt(R**2 - x**2)
    Uz = integrate(f(z), z)
    Ut = integrate(f(t), t)
    assert Ut == Uz.subs(z, t)

