
def test_normality():
    X, Y = Normal('X', 0, 1), Normal('Y', 0, 1)
    x = Symbol('x', real=True)
    z = Symbol('z', real=True)
    dens = density(X - Y, Eq(X + Y, z))

    assert integrate(dens(x), (x, -oo, oo)) == 1

