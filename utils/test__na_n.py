
def test_NaN():
    assert str(nan) == "nan"


def test_NaN():
    assert nan is nan
    assert nan != 1
    assert 1*nan is nan
    assert 1 != nan
    assert -nan is nan
    assert oo != Symbol("x")**3
    assert 2 + nan is nan
    assert 3*nan + 2 is nan
    assert -nan*3 is nan
    assert nan + nan is nan
    assert -nan + nan*(-5) is nan
    assert 8/nan is nan
    raises(TypeError, lambda: nan > 0)
    raises(TypeError, lambda: nan < 0)
    raises(TypeError, lambda: nan >= 0)
    raises(TypeError, lambda: nan <= 0)
    raises(TypeError, lambda: 0 < nan)
    raises(TypeError, lambda: 0 > nan)
    raises(TypeError, lambda: 0 <= nan)
    raises(TypeError, lambda: 0 >= nan)
    assert nan**0 == 1  # as per IEEE 754
    assert 1**nan is nan # IEEE 754 is not the best choice for symbolic work
    # test Pow._eval_power's handling of NaN
    assert Pow(nan, 0, evaluate=False)**2 == 1
    for n in (1, 1., S.One, S.NegativeOne, Float(1)):
        assert n + nan is nan
        assert n - nan is nan
        assert nan + n is nan
        assert nan - n is nan
        assert n/nan is nan
        assert nan/n is nan

