
def test_issue_24266():
    #type1: exp(f(x))
    assert (exp(-I*pi*(2*x+1))).series(x, 0, 3) == -1 + 2*I*pi*x + 2*pi**2*x**2 + O(x**3)
    assert (exp(-I*pi*(2*x+1))*gamma(1+x)).series(x, 0, 3) == -1 + x*(EulerGamma + 2*I*pi) + \
        x**2*(-EulerGamma**2/2 + 23*pi**2/12 - 2*EulerGamma*I*pi) + O(x**3)

    #type2: c**f(x)
    assert ((2*I)**(-I*pi*(2*x+1))).series(x, 0, 2) == exp(pi**2/2 - I*pi*log(2)) + \
          x*(pi**2*exp(pi**2/2 - I*pi*log(2)) - 2*I*pi*exp(pi**2/2 - I*pi*log(2))*log(2)) + O(x**2)
    assert ((2)**(-I*pi*(2*x+1))).series(x, 0, 2) == exp(-I*pi*log(2)) - 2*I*pi*x*exp(-I*pi*log(2))*log(2) + O(x**2)

    #type3: f(y)**g(x)
    assert ((y)**(I*pi*(2*x+1))).series(x, 0, 2) == exp(I*pi*log(y)) + 2*I*pi*x*exp(I*pi*log(y))*log(y) + O(x**2)
    assert ((I*y)**(I*pi*(2*x+1))).series(x, 0, 2) == exp(I*pi*log(I*y)) + 2*I*pi*x*exp(I*pi*log(I*y))*log(I*y) + O(x**2)

