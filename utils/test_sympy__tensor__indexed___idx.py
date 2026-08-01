
def test_sympy__tensor__indexed__Idx():
    from sympy.tensor.indexed import Idx
    assert _test_args(Idx('test'))
    assert _test_args(Idx('test', (0, 10)))
    assert _test_args(Idx('test', 2))
    assert _test_args(Idx('test', x))

