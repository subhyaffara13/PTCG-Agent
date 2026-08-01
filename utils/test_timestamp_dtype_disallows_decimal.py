
def test_timestamp_dtype_disallows_decimal():
    # GH#61773 constructing with pyarrow timestamp dtype should disallow
    #  Decimal NaN, just like pd.to_datetime
    vals = [pd.Timestamp("2016-01-02 03:04:05"), Decimal("NaN")]

    msg = "<class 'decimal.Decimal'> is not convertible to datetime"
    with pytest.raises(TypeError, match=msg):
        # Check that the non-pyarrow version raises as expected
        pd.to_datetime(vals)

    with pytest.raises(TypeError, match=msg):
        pd.array(vals, dtype=ArrowDtype(pa.timestamp("us")))

