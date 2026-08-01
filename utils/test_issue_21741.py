
def test_issue_21741():
    a = 4e6
    b = 2.5e-7
    r = Piecewise((b*I*exp(-a*I*pi*t*y)*exp(-a*I*pi*x*z)/(pi*x), Ne(x, 0)),
                  (z*exp(-a*I*pi*t*y), True))
    fun = E**((-2*I*pi*(z*x+t*y))/(500*10**(-9)))
    assert all_close(integrate(fun, z), r)

