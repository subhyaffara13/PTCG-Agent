
def test_array_copy_on_write():
    df = pd.DataFrame({"a": [decimal.Decimal(2), decimal.Decimal(3)]}, dtype="object")
    df2 = df.astype(DecimalDtype())
    df.iloc[0, 0] = 0
    expected = pd.DataFrame(
        {"a": [decimal.Decimal(2), decimal.Decimal(3)]}, dtype=DecimalDtype()
    )
    tm.assert_equal(df2.values, expected.values)

