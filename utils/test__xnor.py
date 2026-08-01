
def test_Xnor():
    assert Xnor() is true
    assert Xnor(A) == ~A
    assert Xnor(A, A) is true
    assert Xnor(True, A, A) is false
    assert Xnor(A, A, A, A, A) == ~A
    assert Xnor(True) is false
    assert Xnor(False) is true
    assert Xnor(True, True) is true
    assert Xnor(True, False) is false
    assert Xnor(False, False) is true
    assert Xnor(True, A) == A
    assert Xnor(False, A) == ~A
    assert Xnor(True, False, False) is false
    assert Xnor(True, False, A) == A
    assert Xnor(False, False, A) == ~A

