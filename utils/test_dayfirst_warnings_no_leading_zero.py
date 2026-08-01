
def test_dayfirst_warnings_no_leading_zero(date_string, dayfirst):
    # GH47880
    initial_value = f"date\n{date_string}"
    expected = DatetimeIndex(
        ["2014-01-31"], dtype="datetime64[us]", freq=None, name="date"
    )
    warning_msg = (
        "Parsing dates in .* format when dayfirst=.* was specified. "
        "Pass `dayfirst=.*` or specify a format to silence this warning."
    )
    with tm.assert_produces_warning(UserWarning, match=warning_msg):
        res = read_csv(
            StringIO(initial_value),
            parse_dates=["date"],
            index_col="date",
            dayfirst=dayfirst,
        ).index
    tm.assert_index_equal(expected, res)

