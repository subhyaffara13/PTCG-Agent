
def test_Inverse():
    assert Inverse(MatPow(C, 0)).doit() == Identity(n)
    assert Inverse(MatPow(C, 1)).doit() == Inverse(C)
    assert Inverse(MatPow(C, 2)).doit() == MatPow(C, -2)
    assert Inverse(MatPow(C, -1)).doit() == C

    assert MatPow(Inverse(C), 0).doit() == Identity(n)
    assert MatPow(Inverse(C), 1).doit() == Inverse(C)
    assert MatPow(Inverse(C), 2).doit() == MatPow(C, -2)
    assert MatPow(Inverse(C), -1).doit() == C

