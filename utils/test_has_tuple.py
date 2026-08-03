from typing import Tuple

def test_has_tuple():
    assert Tuple(x, y).has(x)
    assert not Tuple(x, y).has(z)
    assert Tuple(f(x), g(x)).has(x)
    assert not Tuple(f(x), g(x)).has(y)
    assert Tuple(f(x), g(x)).has(f)
    assert Tuple(f(x), g(x)).has(f(x))
    # XXX to be deprecated
    #assert not Tuple(f, g).has(x)
    #assert Tuple(f, g).has(f)
    #assert not Tuple(f, g).has(h)
    assert Tuple(True).has(True)
    assert Tuple(True).has(S.true)
    assert not Tuple(True).has(1)

