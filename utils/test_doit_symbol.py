
def test_doit_symbol():
    assert MatPow(C, 0).doit() == Identity(n)
    assert MatPow(C, 1).doit() == C
    assert MatPow(C, -1).doit() == C.I
    for r in [2, S.Half, S.Pi, n]:
        assert MatPow(C, r).doit() == MatPow(C, r)

