
def test_applyfunc_transpose():

    af = Xk.applyfunc(sin)
    assert af.T.dummy_eq(Xk.T.applyfunc(sin))

