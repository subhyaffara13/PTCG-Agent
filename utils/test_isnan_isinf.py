
def test_isnan_isinf():
    x = Symbol('x')

    # isinf
    assert isinf(+S.Infinity) == True
    assert isinf(-S.Infinity) == True
    assert isinf(S.Pi) == False
    isinfx = isinf(x)
    assert isinfx not in (False, True)
    assert isinfx.func is isinf
    assert isinfx.args == (x,)

    # isnan
    assert isnan(S.NaN) == True
    assert isnan(S.Pi) == False
    isnanx = isnan(x)
    assert isnanx not in (False, True)
    assert isnanx.func is isnan
    assert isnanx.args == (x,)

