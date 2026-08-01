
def test_Abs_properties():
    x = Symbol('x')
    assert Abs(x).is_real is None
    assert Abs(x).is_extended_real is True
    assert Abs(x).is_rational is None
    assert Abs(x).is_positive is None
    assert Abs(x).is_nonnegative is None
    assert Abs(x).is_extended_positive is None
    assert Abs(x).is_extended_nonnegative is True

    f = Symbol('x', finite=True)
    assert Abs(f).is_real is True
    assert Abs(f).is_extended_real is True
    assert Abs(f).is_rational is None
    assert Abs(f).is_positive is None
    assert Abs(f).is_nonnegative is True
    assert Abs(f).is_extended_positive is None
    assert Abs(f).is_extended_nonnegative is True

    z = Symbol('z', complex=True, zero=False)
    assert Abs(z).is_real is True # since complex implies finite
    assert Abs(z).is_extended_real is True
    assert Abs(z).is_rational is None
    assert Abs(z).is_positive is True
    assert Abs(z).is_extended_positive is True
    assert Abs(z).is_zero is False

    p = Symbol('p', positive=True)
    assert Abs(p).is_real is True
    assert Abs(p).is_extended_real is True
    assert Abs(p).is_rational is None
    assert Abs(p).is_positive is True
    assert Abs(p).is_zero is False

    q = Symbol('q', rational=True)
    assert Abs(q).is_real is True
    assert Abs(q).is_rational is True
    assert Abs(q).is_integer is None
    assert Abs(q).is_positive is None
    assert Abs(q).is_nonnegative is True

    i = Symbol('i', integer=True)
    assert Abs(i).is_real is True
    assert Abs(i).is_integer is True
    assert Abs(i).is_positive is None
    assert Abs(i).is_nonnegative is True

    e = Symbol('n', even=True)
    ne = Symbol('ne', real=True, even=False)
    assert Abs(e).is_even is True
    assert Abs(ne).is_even is False
    assert Abs(i).is_even is None

    o = Symbol('n', odd=True)
    no = Symbol('no', real=True, odd=False)
    assert Abs(o).is_odd is True
    assert Abs(no).is_odd is False
    assert Abs(i).is_odd is None

