
def test_Add_is_even_odd():
    x = Symbol('x', integer=True)

    k = Symbol('k', odd=True)
    n = Symbol('n', odd=True)
    m = Symbol('m', even=True)

    assert (k + 7).is_even is True
    assert (k + 7).is_odd is False

    assert (-k + 7).is_even is True
    assert (-k + 7).is_odd is False

    assert (k - 12).is_even is False
    assert (k - 12).is_odd is True

    assert (-k - 12).is_even is False
    assert (-k - 12).is_odd is True

    assert (k + n).is_even is True
    assert (k + n).is_odd is False

    assert (k + m).is_even is False
    assert (k + m).is_odd is True

    assert (k + n + m).is_even is True
    assert (k + n + m).is_odd is False

    assert (k + n + x + m).is_even is None
    assert (k + n + x + m).is_odd is None

