
def test_applyfunc_entry():

    af = X.applyfunc(sin)
    assert af[0, 0] == sin(X[0, 0])

    af = Xd.applyfunc(sin)
    assert af[0, 0] == sin(X[0, 0])

