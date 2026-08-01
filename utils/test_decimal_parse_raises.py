
def test_decimal_parse_raises():
    # GH 56984
    ser = pd.Series(["1.2345"], dtype=ArrowDtype(pa.string()))
    with pytest.raises(
        pa.lib.ArrowInvalid, match="Rescaling Decimal(128)? value would cause data loss"
    ):
        ser.astype(ArrowDtype(pa.decimal128(1, 0)))

