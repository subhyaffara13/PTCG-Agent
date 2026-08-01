
def test_issue_19453():
    beta = Symbol("beta", positive=True)
    h = Symbol("h", positive=True)
    m = Symbol("m", positive=True)
    w = Symbol("omega", positive=True)
    g = Symbol("g", positive=True)

    e = exp(1)
    q = 3*h**2*beta*g*e**(0.5*h*beta*w)
    p = m**2*w**2
    s = e**(h*beta*w) - 1
    Z = -q/(4*p*s) - q/(2*p*s**2) - q*(e**(h*beta*w) + 1)/(2*p*s**3)\
            + e**(0.5*h*beta*w)/s
    E = -diff(log(Z), beta)

    assert limit(E - 0.5*h*w, beta, oo) == 0
    assert limit(E.simplify() - 0.5*h*w, beta, oo) == 0

