
def test_attrs():
    a, b = symbols('a, b', cls=Dummy)
    f = Hyper_Function([2, a], [b])
    assert f.ap == Tuple(2, a)
    assert f.bq == Tuple(b)
    assert f.args == (Tuple(2, a), Tuple(b))
    assert f.sizes == (2, 1)

