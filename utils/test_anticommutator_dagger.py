
def test_anticommutator_dagger():
    assert Dagger(AComm(A, B)) == AComm(Dagger(A), Dagger(B))

