
def test_sympy__tensor__indexed__IndexedBase():
    from sympy.tensor.indexed import IndexedBase
    assert _test_args(IndexedBase('A', shape=(x, y)))
    assert _test_args(IndexedBase('A', 1))
    assert _test_args(IndexedBase('A')[0, 1])

