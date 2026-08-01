
def test_dsolve_remove_redundant_solutions():

    eq = (f(x)-2)*f(x).diff(x)
    sol = Eq(f(x), C1)
    assert dsolve(eq) == sol

    eq = (f(x)-sin(x))*(f(x).diff(x, 2))
    sol = {Eq(f(x), C1 + C2*x), Eq(f(x), sin(x))}
    assert set(dsolve(eq)) == sol

    eq = (f(x)**2-2*f(x)+1)*f(x).diff(x, 3)
    sol = Eq(f(x), C1 + C2*x + C3*x**2)
    assert dsolve(eq) == sol

