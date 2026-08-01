
def test_eval_adjoint():
    f = Foo()
    d = Dagger(f)
    assert d == I

