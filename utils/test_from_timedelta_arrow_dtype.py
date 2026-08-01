
def test_from_timedelta_arrow_dtype(unit):
    # GH 54298
    pytest.importorskip("pyarrow")
    expected = Series([timedelta(1)], dtype=f"duration[{unit}][pyarrow]")
    result = to_timedelta(expected)
    tm.assert_series_equal(result, expected)

