
def test_issue_27374():
    #https://github.com/sympy/sympy/issues/27374
    r = sqrt(x**2 + z**2)
    u = erf(a*r/sqrt(2))/r
    Ec = diff(u, z, z).subs([(x, sqrt(b*b-z*z))])
    expected_result = -2*sqrt(2)*b*a**3*exp(-b**2*a**2/2)/(3*sqrt(pi))
    assert simplify(integrate(Ec, (z, -b, b))) == expected_result

