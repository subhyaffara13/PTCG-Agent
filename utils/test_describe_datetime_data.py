
def test_describe_datetime_data(pa_type):
    # GH53001
    data = pd.Series(range(1, 10), dtype=ArrowDtype(pa_type))
    result = data.describe()
    expected = pd.Series(
        [9]
        + [
            pd.Timestamp(v, tz=pa_type.tz, unit=pa_type.unit)
            for v in [5, 1, 3, 5, 7, 9]
        ],
        dtype=object,
        index=["count", "mean", "min", "25%", "50%", "75%", "max"],
    )
    tm.assert_series_equal(result, expected)

