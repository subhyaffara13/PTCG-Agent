
def test_commutator_identities():
    assert AComm(a*A, b*B) == a*b*AComm(A, B)
    assert AComm(A, A) == 2*A**2
    assert AComm(A, B) == AComm(B, A)
    assert AComm(a, b) == 2*a*b
    assert AComm(A, B).doit() == A*B + B*A


def test_commutator_identities():
    assert Comm(a*A, b*B) == a*b*Comm(A, B)
    assert Comm(A, A) == 0
    assert Comm(a, b) == 0
    assert Comm(A, B) == -Comm(B, A)
    assert Comm(A, B).doit() == A*B - B*A
    assert Comm(A, B*C).expand(commutator=True) == Comm(A, B)*C + B*Comm(A, C)
    assert Comm(A*B, C*D).expand(commutator=True) == \
        A*C*Comm(B, D) + A*Comm(B, C)*D + C*Comm(A, D)*B + Comm(A, C)*D*B
    assert Comm(A, B**2).expand(commutator=True) == Comm(A, B)*B + B*Comm(A, B)
    assert Comm(A**2, C**2).expand(commutator=True) == \
        Comm(A*B, C*D).expand(commutator=True).replace(B, A).replace(D, C) == \
        A*C*Comm(A, C) + A*Comm(A, C)*C + C*Comm(A, C)*A + Comm(A, C)*C*A
    assert Comm(A, C**-2).expand(commutator=True) == \
        Comm(A, (1/C)*(1/D)).expand(commutator=True).replace(D, C)
    assert Comm(A + B, C + D).expand(commutator=True) == \
        Comm(A, C) + Comm(A, D) + Comm(B, C) + Comm(B, D)
    assert Comm(A, B + C).expand(commutator=True) == Comm(A, B) + Comm(A, C)
    assert Comm(A**n, B).expand(commutator=True) == Comm(A**n, B)

    e = Comm(A, Comm(B, C)) + Comm(B, Comm(C, A)) + Comm(C, Comm(A, B))
    assert e.doit().expand() == 0

