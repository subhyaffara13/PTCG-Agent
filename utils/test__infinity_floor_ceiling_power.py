
def test_Infinity_floor_ceiling_power():
    assert oo.floor() is oo
    assert oo.ceiling() is oo
    assert oo**S.NaN is S.NaN
    assert oo**zoo is S.NaN

