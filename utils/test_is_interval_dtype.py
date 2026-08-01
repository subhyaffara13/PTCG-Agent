
def test_is_interval_dtype():
    msg = "is_interval_dtype is deprecated"
    with tm.assert_produces_warning(DeprecationWarning, match=msg):
        assert not com.is_interval_dtype(object)
        assert not com.is_interval_dtype([1, 2, 3])

        assert com.is_interval_dtype(IntervalDtype())

        interval = pd.Interval(1, 2, closed="right")
        assert not com.is_interval_dtype(interval)
        assert com.is_interval_dtype(pd.IntervalIndex([interval]))

