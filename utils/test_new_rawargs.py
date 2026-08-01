
def test_new_rawargs():
    n = Symbol('n', commutative=False)
    a = x + n
    assert a.is_commutative is False
    assert a._new_rawargs(x).is_commutative
    assert a._new_rawargs(x, y).is_commutative
    assert a._new_rawargs(x, n).is_commutative is False
    assert a._new_rawargs(x, y, n).is_commutative is False
    m = x*n
    assert m.is_commutative is False
    assert m._new_rawargs(x).is_commutative
    assert m._new_rawargs(n).is_commutative is False
    assert m._new_rawargs(x, y).is_commutative
    assert m._new_rawargs(x, n).is_commutative is False
    assert m._new_rawargs(x, y, n).is_commutative is False

    assert m._new_rawargs(x, n, reeval=False).is_commutative is False
    assert m._new_rawargs(S.One) is S.One

