
def test_issue_15965():
    A = Sum(z*x**y, (x, 1, a))
    anew = z*Sum(x**y, (x, 1, a))
    B = Integral(x*y, x)
    bdo = x**2*y/2
    assert simplify(A + B) == anew + bdo
    assert simplify(A) == anew
    assert simplify(B) == bdo
    assert simplify(B, doit=False) == y*Integral(x, x)

