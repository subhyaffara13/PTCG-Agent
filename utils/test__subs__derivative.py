
def test_Subs_Derivative():
    a = Derivative(f(g(x), h(x)), g(x), h(x),x)
    b = Derivative(Derivative(f(g(x), h(x)), g(x), h(x)),x)
    c = f(g(x), h(x)).diff(g(x), h(x), x)
    d = f(g(x), h(x)).diff(g(x), h(x)).diff(x)
    e = Derivative(f(g(x), h(x)), x)
    eqs = (a, b, c, d, e)
    subs = lambda arg: arg.subs(f, Lambda((x, y), exp(x + y))
        ).subs(g(x), 1/x).subs(h(x), x**3)
    ans = 3*x**2*exp(1/x)*exp(x**3) - exp(1/x)*exp(x**3)/x**2
    assert all(subs(i).doit().expand() == ans for i in eqs)
    assert all(subs(i.doit()).doit().expand() == ans for i in eqs)

