
def test_iter_temporal(pa_type):
    # GH 53326
    arr = ArrowExtensionArray(pa.array([1, None], type=pa_type))
    result = list(arr)
    if pa.types.is_duration(pa_type):
        expected = [
            pd.Timedelta(1, unit=pa_type.unit).as_unit(pa_type.unit),
            pd.NA,
        ]
        assert isinstance(result[0], pd.Timedelta)
    else:
        expected = [
            pd.Timestamp(1, unit=pa_type.unit, tz=pa_type.tz).as_unit(pa_type.unit),
            pd.NA,
        ]
        assert isinstance(result[0], pd.Timestamp)
    assert result[0].unit == expected[0].unit
    assert result == expected

