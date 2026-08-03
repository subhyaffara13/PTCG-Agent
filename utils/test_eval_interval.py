from typing import Tuple

def test_eval_interval():
    assert exp(x)._eval_interval(*Tuple(x, 0, 1)) == exp(1) - exp(0)

    # issue 4199
    a = x/y
    raises(NotImplementedError, lambda: a._eval_interval(x, S.Zero, oo)._eval_interval(y, oo, S.Zero))
    raises(NotImplementedError, lambda: a._eval_interval(x, S.Zero, oo)._eval_interval(y, S.Zero, oo))
    a = x - y
    raises(NotImplementedError, lambda: a._eval_interval(x, S.One, oo)._eval_interval(y, oo, S.One))
    raises(ValueError, lambda: x._eval_interval(x, None, None))
    a = -y*Heaviside(x - y)
    assert a._eval_interval(x, -oo, oo) == -y
    assert a._eval_interval(x, oo, -oo) == y

