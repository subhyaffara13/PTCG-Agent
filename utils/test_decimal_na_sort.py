
def test_decimal_na_sort(test_series):
    # GH#54847
    # We catch both TypeError and decimal.InvalidOperation exceptions in safe_sort.
    # If this next assert raises, we can just catch TypeError
    assert not isinstance(decimal.InvalidOperation, TypeError)
    df = DataFrame(
        {
            "key": [Decimal(1), Decimal(1), None, None],
            "value": [Decimal(2), Decimal(3), Decimal(4), Decimal(5)],
        }
    )
    gb = df.groupby("key", dropna=False)
    if test_series:
        gb = gb["value"]
    result = gb._grouper.result_index
    expected = Index([Decimal(1), None], name="key")
    tm.assert_index_equal(result, expected)

