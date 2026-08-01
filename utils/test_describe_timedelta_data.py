
def test_describe_timedelta_data(pa_type):
    # GH53001
    data = pd.Series(range(1, 10), dtype=ArrowDtype(pa_type))
    result = data.describe()
    expected = pd.Series(
        [9, *pd.to_timedelta([5, 2, 1, 3, 5, 7, 9], unit=pa_type.unit).tolist()],
        dtype=object,
        index=["count", "mean", "std", "min", "25%", "50%", "75%", "max"],
    )
    tm.assert_series_equal(result, expected)

