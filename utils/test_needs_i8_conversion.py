
def test_needs_i8_conversion():
    assert not com.needs_i8_conversion(str)
    assert not com.needs_i8_conversion(np.int64)
    assert not com.needs_i8_conversion(pd.Series([1, 2]))
    assert not com.needs_i8_conversion(np.array(["a", "b"]))

    assert not com.needs_i8_conversion(np.datetime64)
    assert com.needs_i8_conversion(np.dtype(np.datetime64))
    assert not com.needs_i8_conversion(pd.Series([], dtype="timedelta64[ns]"))
    assert com.needs_i8_conversion(pd.Series([], dtype="timedelta64[ns]").dtype)
    assert not com.needs_i8_conversion(pd.DatetimeIndex(["2000"], tz="US/Eastern"))
    assert com.needs_i8_conversion(pd.DatetimeIndex(["2000"], tz="US/Eastern").dtype)

