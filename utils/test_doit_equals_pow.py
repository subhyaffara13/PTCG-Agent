
def test_doit_equals_pow(): #17179
    X = ImmutableMatrix ([[1,0],[0,1]])
    assert MatPow(X, n).doit() == X**n == X

