
def test_dayfirst_warnings():
    # GH 12585

    # CASE 1: valid input
    input = "date\n31/12/2014\n10/03/2011"
    expected = DatetimeIndex(
        ["2014-12-31", "2011-03-10"], dtype="datetime64[us]", freq=None, name="date"
    )
    warning_msg = (
        "Parsing dates in .* format when dayfirst=.* was specified. "
        "Pass `dayfirst=.*` or specify a format to silence this warning."
    )

    # A. dayfirst arg correct, no warning
    res1 = read_csv(
        StringIO(input), parse_dates=["date"], dayfirst=True, index_col="date"
    ).index
    tm.assert_index_equal(expected, res1)

    # B. dayfirst arg incorrect, warning
    with tm.assert_produces_warning(UserWarning, match=warning_msg):
        res2 = read_csv(
            StringIO(input), parse_dates=["date"], dayfirst=False, index_col="date"
        ).index
    tm.assert_index_equal(expected, res2)

    # CASE 2: invalid input
    # cannot consistently process with single format
    # return to user unaltered

    # first in DD/MM/YYYY, second in MM/DD/YYYY
    input = "date\n31/12/2014\n03/30/2011"
    expected = Index(["31/12/2014", "03/30/2011"], dtype="str", name="date")

    # A. use dayfirst=True
    res5 = read_csv(
        StringIO(input), parse_dates=["date"], dayfirst=True, index_col="date"
    ).index
    tm.assert_index_equal(expected, res5)

    # B. use dayfirst=False
    with tm.assert_produces_warning(UserWarning, match=warning_msg):
        res6 = read_csv(
            StringIO(input), parse_dates=["date"], dayfirst=False, index_col="date"
        ).index
    tm.assert_index_equal(expected, res6)

