
def test_Equivalent():
    assert str(Equivalent(y, x)) == "Equivalent(x, y)"


def test_Equivalent():
    assert Equivalent(A, B) == Equivalent(B, A) == Equivalent(A, B, A)
    assert Equivalent() is true
    assert Equivalent(A, A) == Equivalent(A) is true
    assert Equivalent(True, True) == Equivalent(False, False) is true
    assert Equivalent(True, False) == Equivalent(False, True) is false
    assert Equivalent(A, True) == A
    assert Equivalent(A, False) == Not(A)
    assert Equivalent(A, B, True) == A & B
    assert Equivalent(A, B, False) == ~A & ~B
    assert Equivalent(1, A) == A
    assert Equivalent(0, A) == Not(A)
    assert Equivalent(A, Equivalent(B, C)) != Equivalent(Equivalent(A, B), C)
    assert Equivalent(A < 1, A >= 1) is false
    assert Equivalent(A < 1, A >= 1, 0) is false
    assert Equivalent(A < 1, A >= 1, 1) is false
    assert Equivalent(A < 1, S.One > A) == Equivalent(1, 1) == Equivalent(0, 0)
    assert Equivalent(Equality(A, B), Equality(B, A)) is true

