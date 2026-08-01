
def test_issue_17141():
    # Check that there is no RecursionError
    assert simplify(x**(1 / acos(I))) == x**(2/(pi - 2*I*log(1 + sqrt(2))))
    assert simplify(acos(-I)**2*acos(I)**2) == \
           log(1 + sqrt(2))**4 + pi**2*log(1 + sqrt(2))**2/2 + pi**4/16
    assert simplify(2**acos(I)**2) == 2**((pi - 2*I*log(1 + sqrt(2)))**2/4)
    p = 2**acos(I+1)**2
    assert simplify(p) == p

