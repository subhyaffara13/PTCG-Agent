
def test_issue_18361():
    A = Array([sin(2 * x) - 2 * sin(x) * cos(x)])
    B = Array([sin(x)**2 + cos(x)**2, 0])
    C = Array([(x + x**2)/(x*sin(y)**2 + x*cos(y)**2), 2*sin(x)*cos(x)])
    assert simplify(A) == Array([0])
    assert simplify(B) == Array([1, 0])
    assert simplify(C) == Array([x + 1, sin(2*x)])

