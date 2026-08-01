
def test_One_power():
    assert S.One**12 is S.One
    assert S.NegativeOne**S.NaN is S.NaN

