
def test_Implies():
    raises(ValueError, lambda: Implies(A, B, C))
    assert Implies(True, True) is true
    assert Implies(True, False) is false
    assert Implies(False, True) is true
    assert Implies(False, False) is true
    assert Implies(0, A) is true
    assert Implies(1, 1) is true
    assert Implies(1, 0) is false
    assert A >> B == B << A
    assert (A < 1) >> (A >= 1) == (A >= 1)
    assert (A < 1) >> (S.One > A) is true
    assert A >> A is true

