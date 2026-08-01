
def test_Xor():
    assert str(Xor(y, x, evaluate=False)) == "x ^ y"


def test_Xor():
    assert Xor() is false
    assert Xor(A) == A
    assert Xor(A, A) is false
    assert Xor(True, A, A) is true
    assert Xor(A, A, A, A, A) == A
    assert Xor(True, False, False, A, B) == ~Xor(A, B)
    assert Xor(True) is true
    assert Xor(False) is false
    assert Xor(True, True) is false
    assert Xor(True, False) is true
    assert Xor(False, False) is false
    assert Xor(True, A) == ~A
    assert Xor(False, A) == A
    assert Xor(True, False, False) is true
    assert Xor(True, False, A) == ~A
    assert Xor(False, False, A) == A
    assert isinstance(Xor(A, B), Xor)
    assert Xor(A, B, Xor(C, D)) == Xor(A, B, C, D)
    assert Xor(A, B, Xor(B, C)) == Xor(A, C)
    assert Xor(A < 1, A >= 1, B) == Xor(0, 1, B) == Xor(1, 0, B)
    e = A > 1
    assert Xor(e, e.canonical) == Xor(0, 0) == Xor(1, 1)

