
def test_Add_Mul_is_integer():
    x = Symbol('x')

    k = Symbol('k', integer=True)
    n = Symbol('n', integer=True)
    nk = Symbol('nk', integer=False)
    nr = Symbol('nr', rational=False)
    nz = Symbol('nz', integer=True, zero=False)

    assert (-nk).is_integer is None
    assert (-nr).is_integer is False
    assert (2*k).is_integer is True
    assert (-k).is_integer is True

    assert (k + nk).is_integer is False
    assert (k + n).is_integer is True
    assert (k + x).is_integer is None
    assert (k + n*x).is_integer is None
    assert (k + n/3).is_integer is None
    assert (k + nz/3).is_integer is None
    assert (k + nr/3).is_integer is False

    assert ((1 + sqrt(3))*(-sqrt(3) + 1)).is_integer is not False
    assert (1 + (1 + sqrt(3))*(-sqrt(3) + 1)).is_integer is not False

