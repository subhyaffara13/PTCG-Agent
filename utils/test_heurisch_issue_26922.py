
def test_heurisch_issue_26922():

    a, b, x = symbols("a, b, x", real=True, positive=True)
    C = symbols("C", real=True)
    i1 = -C*x*exp(-a*x**2 - sqrt(b)*x)
    i2 = C*x*exp(-a*x**2 + sqrt(b)*x)
    i = Integral(i1, x) + Integral(i2, x)
    res = (
        -C*exp(-a*x**2)*exp(sqrt(b)*x)/(2*a)
        + C*exp(-a*x**2)*exp(-sqrt(b)*x)/(2*a)
        + sqrt(pi)*C*sqrt(b)*exp(b/(4*a))*erf(sqrt(a)*x - sqrt(b)/(2*sqrt(a)))/(4*a**(S(3)/2))
        + sqrt(pi)*C*sqrt(b)*exp(b/(4*a))*erf(sqrt(a)*x + sqrt(b)/(2*sqrt(a)))/(4*a**(S(3)/2))
    )

    assert i.doit(heurisch=False).expand() == res

