
def test_issue_5817():
    a, b, c = symbols('a,b,c', positive=True)

    assert simplify(ratint(a/(b*c*x**2 + a**2 + b*a), x)) == \
        sqrt(a)*atan(sqrt(
            b)*sqrt(c)*x/(sqrt(a)*sqrt(a + b)))/(sqrt(b)*sqrt(c)*sqrt(a + b))

