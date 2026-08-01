
def test_Pow_is_pos_neg():
    z = Symbol('z', real=True)
    w = Symbol('w', nonpositive=True)

    assert (S.NegativeOne**S(2)).is_positive is True
    assert (S.One**z).is_positive is True
    assert (S.NegativeOne**S(3)).is_positive is False
    assert (S.Zero**S.Zero).is_positive is True  # 0**0 is 1
    assert (w**S(3)).is_positive is False
    assert (w**S(2)).is_positive is None
    assert (I**2).is_positive is False
    assert (I**4).is_positive is True

    # tests emerging from #16332 issue
    p = Symbol('p', zero=True)
    q = Symbol('q', zero=False, real=True)
    j = Symbol('j', zero=False, even=True)
    x = Symbol('x', zero=True)
    y = Symbol('y', zero=True)
    assert (p**q).is_positive is False
    assert (p**q).is_negative is False
    assert (p**j).is_positive is False
    assert (x**y).is_positive is True   # 0**0
    assert (x**y).is_negative is False

