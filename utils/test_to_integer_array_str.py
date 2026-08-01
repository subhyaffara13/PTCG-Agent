
def test_to_integer_array_str():
    result = IntegerArray._from_sequence(["1", "2", None], dtype="Int64")
    expected = pd.array([1, 2, pd.NA], dtype="Int64")
    tm.assert_extension_array_equal(result, expected)

    with pytest.raises(
        ValueError, match=r"invalid literal for int\(\) with base 10: .*"
    ):
        IntegerArray._from_sequence(["1", "2", ""], dtype="Int64")

    with pytest.raises(
        ValueError, match=r"invalid literal for int\(\) with base 10: .*"
    ):
        IntegerArray._from_sequence(["1.5", "2.0"], dtype="Int64")

