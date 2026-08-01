
def test_applyfunc_as_explicit():

    af = X.applyfunc(sin)
    assert af.as_explicit() == Matrix([
        [sin(X[0, 0]), sin(X[0, 1]), sin(X[0, 2])],
        [sin(X[1, 0]), sin(X[1, 1]), sin(X[1, 2])],
        [sin(X[2, 0]), sin(X[2, 1]), sin(X[2, 2])],
    ])

