
def test_nargs():
    f = Function('f')
    assert f.nargs == S.Naturals0
    assert f(1).nargs == S.Naturals0
    assert Function('f', nargs=2)(1, 2).nargs == FiniteSet(2)
    assert sin.nargs == FiniteSet(1)
    assert sin(2).nargs == FiniteSet(1)
    assert log.nargs == FiniteSet(1, 2)
    assert log(2).nargs == FiniteSet(1, 2)
    assert Function('f', nargs=2).nargs == FiniteSet(2)
    assert Function('f', nargs=0).nargs == FiniteSet(0)
    assert Function('f', nargs=(0, 1)).nargs == FiniteSet(0, 1)
    assert Function('f', nargs=None).nargs == S.Naturals0
    raises(ValueError, lambda: Function('f', nargs=()))

