
def test_arrow_array():
    pa = pytest.importorskip("pyarrow")

    from pandas.core.arrays.arrow.extension_types import ArrowIntervalType

    intervals = pd.interval_range(1, 5, freq=1).array

    result = pa.array(intervals)
    assert isinstance(result.type, ArrowIntervalType)
    assert result.type.closed == intervals.closed
    assert result.type.subtype == pa.int64()
    assert result.storage.field("left").equals(pa.array([1, 2, 3, 4], type="int64"))
    assert result.storage.field("right").equals(pa.array([2, 3, 4, 5], type="int64"))

    expected = pa.array([{"left": i, "right": i + 1} for i in range(1, 5)])
    assert result.storage.equals(expected)

    # convert to its storage type
    result = pa.array(intervals, type=expected.type)
    assert result.equals(expected)

    # unsupported conversions
    with pytest.raises(TypeError, match="Not supported to convert IntervalArray"):
        pa.array(intervals, type="float64")

    with pytest.raises(TypeError, match="Not supported to convert IntervalArray"):
        pa.array(intervals, type=ArrowIntervalType(pa.float64(), "left"))


def test_arrow_array(data):
    arr = pa.array(data)
    expected = pa.array(
        data.to_numpy(object, na_value=None),
        type=pa.from_numpy_dtype(data.dtype.numpy_dtype),
    )
    assert arr.equals(expected)


def test_arrow_array(data, freq):
    from pandas.core.arrays.arrow.extension_types import ArrowPeriodType

    periods = period_array(data, freq=freq)
    result = pa.array(periods)
    assert isinstance(result.type, ArrowPeriodType)
    assert result.type.freq == freq
    expected = pa.array(periods.asi8, type="int64")
    assert result.storage.equals(expected)

    # convert to its storage type
    result = pa.array(periods, type=pa.int64())
    assert result.equals(expected)

    # unsupported conversions
    msg = "Not supported to convert PeriodArray to 'double' type"
    with pytest.raises(TypeError, match=msg):
        pa.array(periods, type="float64")


def test_arrow_array(dtype):
    # protocol added in 0.15.0
    pa = pytest.importorskip("pyarrow")
    import pyarrow.compute as pc

    data = pd.array(["a", "b", "c"], dtype=dtype)
    arr = pa.array(data)
    expected = pa.array(list(data), type=pa.large_string(), from_pandas=True)
    if dtype.storage == "python":
        expected = pc.cast(expected, pa.string())
    assert arr.equals(expected)

