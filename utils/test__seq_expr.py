from typing import Tuple

def test_SeqExpr():
    #SeqExpr is a baseclass and does not take care of
    #ensuring all arguments are Basics hence the use of
    #Tuple(...) here.
    s = SeqExpr(Tuple(1, n, y), Tuple(x, 0, 10))

    assert isinstance(s, SeqExpr)
    assert s.gen == (1, n, y)
    assert s.interval == Interval(0, 10)
    assert s.start == 0
    assert s.stop == 10
    assert s.length == 11
    assert s.variables == (x,)

    assert SeqExpr(Tuple(1, 2, 3), Tuple(x, 0, oo)).length is oo

