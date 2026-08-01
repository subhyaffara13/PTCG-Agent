
def test_rolling_skew_eq_value_fperr(step):
    # #18804 all rolling skew for all equal values should return Nan
    # #46717 update: all equal values should return 0 instead of NaN
    a = Series([1.1] * 15).rolling(window=10, step=step).skew()
    assert (a[a.index >= 9] == 0).all()
    assert a[a.index < 9].isna().all()

