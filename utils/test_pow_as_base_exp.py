
def test_pow_as_base_exp():
    assert (S.Infinity**(2 - x)).as_base_exp() == (S.Infinity, 2 - x)
    assert (S.Infinity**(x - 2)).as_base_exp() == (S.Infinity, x - 2)
    p = S.Half**x
    assert p.base, p.exp == p.as_base_exp() == (S(2), -x)
    p = (S(3)/2)**x
    assert p.base, p.exp == p.as_base_exp() == (3*S.Half, x)
    p = (S(2)/3)**x
    assert p.as_base_exp() == (S(2)/3, x)
    assert p.base, p.exp == (S(2)/3, x)
    # issue 8344:
    assert Pow(1, 2, evaluate=False).as_base_exp() == (S.One, S(2))

