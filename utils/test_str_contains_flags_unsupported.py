
def test_str_contains_flags_unsupported():
    ser = pd.Series(["abc", None], dtype=ArrowDtype(pa.string()))
    with pytest.raises(NotImplementedError, match="contains not"):
        ser.str.contains("a", flags=1)

