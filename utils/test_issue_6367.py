
def test_issue_6367():
    z = -5*sqrt(2)/(2*sqrt(2*sqrt(29) + 29)) + sqrt(-sqrt(29)/29 + S.Half)
    assert Mul(*[powsimp(a) for a in Mul.make_args(z.normal())]) == 0
    assert powsimp(z.normal()) == 0
    assert simplify(z) == 0
    assert powsimp(sqrt(2 + sqrt(3))*sqrt(2 - sqrt(3)) + 1) == 2
    assert powsimp(z) != 0

