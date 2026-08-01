
def test_commutator_dagger():
    comm = Comm(A*B, C)
    assert Dagger(comm).expand(commutator=True) == \
        - Comm(Dagger(B), Dagger(C))*Dagger(A) - \
        Dagger(B)*Comm(Dagger(A), Dagger(C))

