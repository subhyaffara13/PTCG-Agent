
def test_Mul_is_even_odd():
    x = Symbol('x', integer=True)
    y = Symbol('y', integer=True)

    k = Symbol('k', odd=True)
    n = Symbol('n', odd=True)
    m = Symbol('m', even=True)

    assert (2*x).is_even is True
    assert (2*x).is_odd is False

    assert (3*x).is_even is None
    assert (3*x).is_odd is None

    assert (k/3).is_integer is None
    assert (k/3).is_even is None
    assert (k/3).is_odd is None

    assert (2*n).is_even is True
    assert (2*n).is_odd is False

    assert (2*m).is_even is True
    assert (2*m).is_odd is False

    assert (-n).is_even is False
    assert (-n).is_odd is True

    assert (k*n).is_even is False
    assert (k*n).is_odd is True

    assert (k*m).is_even is True
    assert (k*m).is_odd is False

    assert (k*n*m).is_even is True
    assert (k*n*m).is_odd is False

    assert (k*m*x).is_even is True
    assert (k*m*x).is_odd is False

    # issue 6791:
    assert (x/2).is_integer is None
    assert (k/2).is_integer is False
    assert (m/2).is_integer is True

    assert (x*y).is_even is None
    assert (x*x).is_even is None
    assert (x*(x + k)).is_even is True
    assert (x*(x + m)).is_even is None

    assert (x*y).is_odd is None
    assert (x*x).is_odd is None
    assert (x*(x + k)).is_odd is False
    assert (x*(x + m)).is_odd is None

    # issue 8648
    assert (m**2/2).is_even
    assert (m**2/3).is_even is False
    assert (2/m**2).is_odd is False
    assert (2/m).is_odd is None

