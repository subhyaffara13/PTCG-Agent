
def test_issue_7971_21740():
    z = Integral(x, (x, 1, 1))
    assert z != 0
    assert simplify(z) is S.Zero
    assert simplify(S.Zero) is S.Zero
    z = simplify(Float(0))
    assert z is not S.Zero and z == 0.0

