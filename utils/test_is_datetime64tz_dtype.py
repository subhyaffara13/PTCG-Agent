
def test_is_datetime64tz_dtype():
    msg = "is_datetime64tz_dtype is deprecated"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        assert not com.is_datetime64tz_dtype(object)
        assert not com.is_datetime64tz_dtype([1, 2, 3])
        assert not com.is_datetime64tz_dtype(pd.DatetimeIndex([1, 2, 3]))
        assert com.is_datetime64tz_dtype(pd.DatetimeIndex(["2000"], tz="US/Eastern"))

