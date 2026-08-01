
def test_pde_separate():
    x, y, z, t = symbols("x,y,z,t")
    F, T, X, Y, Z, u = map(Function, 'FTXYZu')

    eq = Eq(D(u(x, t), x), D(u(x, t), t)*exp(u(x, t)))
    raises(ValueError, lambda: pde_separate(eq, u(x, t), [X(x), T(t)], 'div'))

