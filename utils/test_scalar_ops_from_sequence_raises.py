
def test_scalar_ops_from_sequence_raises():
    # op(EA, EA) should return an EA, or an ndarray if it's not possible
    # to return an EA with the return values.
    arr = DecimalArrayWithoutCoercion([decimal.Decimal("1.0"), decimal.Decimal("2.0")])
    result = arr + arr
    expected = np.array(
        [decimal.Decimal("2.0"), decimal.Decimal("4.0")], dtype="object"
    )
    tm.assert_numpy_array_equal(result, expected)

