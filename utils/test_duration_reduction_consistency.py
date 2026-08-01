
def test_duration_reduction_consistency(unit, method):
    # GH#63170
    dtype = f"duration[{unit}][pyarrow]"
    ser = pd.Series([timedelta(seconds=1), timedelta(seconds=2)], dtype=dtype)
    result = getattr(ser, method)()
    assert isinstance(result, pd.Timedelta), (
        f"{method} for {unit} returned {type(result)}"
    )
    assert result.unit == unit

