
def test_timestamp_reduction_consistency(unit, method):
    # GH#63170
    dtype = f"timestamp[{unit}][pyarrow]"
    ser = pd.Series([datetime(2024, 1, 1), datetime(2024, 1, 3)], dtype=dtype)
    result = getattr(ser, method)()
    assert isinstance(result, pd.Timestamp), (
        f"{method} for {unit} returned {type(result)}"
    )
    assert result.unit == unit

