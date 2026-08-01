
def test_issue_14025():
    a, b, c, d = symbols('a,b,c,d', commutative=False)
    assert Mul(a, b, c).has(c*b) == False
    assert Mul(a, b, c).has(b*c) == True
    assert Mul(a, b, c, d).has(b*c*d) == True

