
def test_as_set():
    x = Symbol('x')
    y = Symbol('y')
    assert Contains(x, FiniteSet(y)).as_set() == FiniteSet(y)
    assert Contains(x, S.Integers).as_set() == S.Integers
    assert Contains(x, S.Reals).as_set() == S.Reals

