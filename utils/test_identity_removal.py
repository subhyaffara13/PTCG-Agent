
def test_identity_removal():
    assert Add.make_args(x + 0) == (x,)
    assert Mul.make_args(x*1) == (x,)

