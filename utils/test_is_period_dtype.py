
def test_is_period_dtype():
    msg = "is_period_dtype is deprecated"
    with tm.assert_produces_warning(DeprecationWarning, match=msg):
        assert not com.is_period_dtype(object)
        assert not com.is_period_dtype([1, 2, 3])
        assert not com.is_period_dtype(pd.Period("2017-01-01"))

        assert com.is_period_dtype(PeriodDtype(freq="D"))
        assert com.is_period_dtype(pd.PeriodIndex([], freq="Y"))

