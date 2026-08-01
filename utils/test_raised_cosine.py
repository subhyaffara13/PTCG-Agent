
def test_raised_cosine():
    mu = Symbol("mu", real=True)
    s = Symbol("s", positive=True)

    X = RaisedCosine("x", mu, s)

    assert pspace(X).domain.set == Interval(mu - s, mu + s)
    #Tests characteristics_function
    assert characteristic_function(X)(x) == \
           Piecewise((exp(-I*pi*mu/s)/2, Eq(x, -pi/s)), (exp(I*pi*mu/s)/2, Eq(x, pi/s)), (pi**2*exp(I*mu*x)*sin(s*x)/(s*x*(-s**2*x**2 + pi**2)), True))

    assert density(X)(x) == (Piecewise(((cos(pi*(x - mu)/s) + 1)/(2*s),
                          And(x <= mu + s, mu - s <= x)), (0, True)))

