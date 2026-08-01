
def test_eval_commutator():
    F = Foo('F')
    B = Bar('B')
    T = Tam('T')
    assert AComm(F, B).doit() == 0
    assert AComm(B, F).doit() == 0
    assert AComm(F, T).doit() == 1
    assert AComm(T, F).doit() == 1
    assert AComm(B, T).doit() == B*T + T*B


def test_eval_commutator():
    F = Foo('F')
    B = Bar('B')
    T = Tam('T')
    assert Comm(F, B).doit() == 0
    assert Comm(B, F).doit() == 0
    assert Comm(F, T).doit() == -1
    assert Comm(T, F).doit() == 1
    assert Comm(B, T).doit() == B*T - T*B
    assert Comm(F**2, B).expand(commutator=True).doit() == 0
    assert Comm(F**2, T).expand(commutator=True).doit() == -2*F
    assert Comm(F, T**2).expand(commutator=True).doit() == -2*T
    assert Comm(T**2, F).expand(commutator=True).doit() == 2*T
    assert Comm(T**2, F**3).expand(commutator=True).doit() == 2*F*T*F + 2*F**2*T + 2*T*F**2

