
def test_arrowextensiondtype_dataframe_repr():
    # GH 54062
    df = pd.DataFrame(
        pd.period_range("2012", periods=3),
        columns=["col"],
        dtype=ArrowDtype(ArrowPeriodType("D")),
    )
    result = repr(df)
    # TODO: repr value may not be expected; address how
    # pyarrow.ExtensionType values are displayed
    expected = "     col\n0  15340\n1  15341\n2  15342"
    assert result == expected

