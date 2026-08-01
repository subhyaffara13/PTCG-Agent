
def test_Infinity_inequations():
    assert oo > pi
    assert not (oo < pi)
    assert exp(-3) < oo

    assert _inf > pi
    assert not (_inf < pi)
    assert exp(-3) < _inf

    raises(TypeError, lambda: oo < I)
    raises(TypeError, lambda: oo <= I)
    raises(TypeError, lambda: oo > I)
    raises(TypeError, lambda: oo >= I)
    raises(TypeError, lambda: -oo < I)
    raises(TypeError, lambda: -oo <= I)
    raises(TypeError, lambda: -oo > I)
    raises(TypeError, lambda: -oo >= I)

    raises(TypeError, lambda: I < oo)
    raises(TypeError, lambda: I <= oo)
    raises(TypeError, lambda: I > oo)
    raises(TypeError, lambda: I >= oo)
    raises(TypeError, lambda: I < -oo)
    raises(TypeError, lambda: I <= -oo)
    raises(TypeError, lambda: I > -oo)
    raises(TypeError, lambda: I >= -oo)

    assert oo > -oo and oo >= -oo
    assert (oo < -oo) == False and (oo <= -oo) == False
    assert -oo < oo and -oo <= oo
    assert (-oo > oo) == False and (-oo >= oo) == False

    assert (oo < oo) == False  # issue 7775
    assert (oo > oo) == False
    assert (-oo > -oo) == False and (-oo < -oo) == False
    assert oo >= oo and oo <= oo and -oo >= -oo and -oo <= -oo
    assert (-oo < -_inf) ==  False
    assert (oo > _inf) == False
    assert -oo >= -_inf
    assert oo <= _inf

    x = Symbol('x')
    b = Symbol('b', finite=True, real=True)
    assert (x < oo) == Lt(x, oo)  # issue 7775
    assert b < oo and b > -oo and b <= oo and b >= -oo
    assert oo > b and oo >= b and (oo < b) == False and (oo <= b) == False
    assert (-oo > b) == False and (-oo >= b) == False and -oo < b and -oo <= b
    assert (oo < x) == Lt(oo, x) and (oo > x) == Gt(oo, x)
    assert (oo <= x) == Le(oo, x) and (oo >= x) == Ge(oo, x)
    assert (-oo < x) == Lt(-oo, x) and (-oo > x) == Gt(-oo, x)
    assert (-oo <= x) == Le(-oo, x) and (-oo >= x) == Ge(-oo, x)

