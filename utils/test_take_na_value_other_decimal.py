
def test_take_na_value_other_decimal():
    arr = DecimalArray([decimal.Decimal("1.0"), decimal.Decimal("2.0")])
    result = arr.take([0, -1], allow_fill=True, fill_value=decimal.Decimal("-1.0"))
    expected = DecimalArray([decimal.Decimal("1.0"), decimal.Decimal("-1.0")])
    tm.assert_extension_array_equal(result, expected)

