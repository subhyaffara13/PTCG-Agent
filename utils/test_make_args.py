
def test_make_args():
    assert Add.make_args(x) == (x,)
    assert Mul.make_args(x) == (x,)

    assert Add.make_args(x*y*z) == (x*y*z,)
    assert Mul.make_args(x*y*z) == (x*y*z).args

    assert Add.make_args(x + y + z) == (x + y + z).args
    assert Mul.make_args(x + y + z) == (x + y + z,)

    assert Add.make_args((x + y)**z) == ((x + y)**z,)
    assert Mul.make_args((x + y)**z) == ((x + y)**z,)

