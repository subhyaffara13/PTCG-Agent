
def test_issue_6121():
    eq = -I*exp(-3*I*pi/4)/(4*pi**(S(3)/2)*sqrt(x))
    assert eq.expand(complex=True)  # does not give oo recursion
    eq = -I*exp(-3*I*pi/4)/(4*pi**(R(3, 2))*sqrt(x))
    assert eq.expand(complex=True)  # does not give oo recursion

