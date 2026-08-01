
def test_bypass_non_commutatives():
    A, B, C = symbols('A B C', commutative=False)
    l = [A*B*C, A*C]
    assert cse(l) == ([], l)
    l = [A*B*C, A*B]
    assert cse(l) == ([], l)
    l = [B*C, A*B*C]
    assert cse(l) == ([], l)

