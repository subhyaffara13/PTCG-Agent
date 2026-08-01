
def test_issue_13733():
    s = Symbol('s', positive=True)
    pz = exp(-(z - y)**2/(2*s*s))/sqrt(2*pi*s*s)
    pzgx = integrate(pz, (z, x, oo))
    assert integrate(pzgx, (x, 0, oo)) == sqrt(2)*s*exp(-y**2/(2*s**2))/(2*sqrt(pi)) + \
        y*erf(sqrt(2)*y/(2*s))/2 + y/2

