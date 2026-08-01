
def test_issue_7724():
    eq = Poly(x**4*I + x**2 + I, x)
    assert roots(eq) == {
        sqrt(I/2 + sqrt(5)*I/2): 1,
        sqrt(-sqrt(5)*I/2 + I/2): 1,
        -sqrt(I/2 + sqrt(5)*I/2): 1,
        -sqrt(-sqrt(5)*I/2 + I/2): 1}

