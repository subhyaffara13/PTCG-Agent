
def test_issue_6122():
    assert integrate(exp(-I*x**2), (x, -oo, oo), meijerg=True) == \
        -I*sqrt(pi)*exp(I*pi/4)

