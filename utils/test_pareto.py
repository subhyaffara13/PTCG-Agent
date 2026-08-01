
def test_pareto():
    xm, beta = symbols('xm beta', positive=True)
    alpha = beta + 5
    X = Pareto('x', xm, alpha)

    dens = density(X)

    #Tests cdf function
    assert cdf(X)(x) == \
           Piecewise((-x**(-beta - 5)*xm**(beta + 5) + 1, x >= xm), (0, True))

    #Tests characteristic_function
    assert characteristic_function(X)(x) == \
           ((-I*x*xm)**(beta + 5)*(beta + 5)*uppergamma(-beta - 5, -I*x*xm))

    assert dens(x) == x**(-(alpha + 1))*xm**(alpha)*(alpha)

    assert simplify(E(X)) == alpha*xm/(alpha-1)

