
def test_normalize_bad_arg_raises(any_string_dtype):
    ser = Series(
        ["ABC", "ＡＢＣ", "１２３", np.nan, "ｱｲｴ"],  # noqa: RUF001
        index=["a", "b", "c", "d", "e"],
        dtype=any_string_dtype,
    )
    with pytest.raises(ValueError, match="invalid normalization form"):
        ser.str.normalize("xxx")

