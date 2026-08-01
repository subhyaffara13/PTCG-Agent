
def test_str_count_flags_unsupported():
    ser = pd.Series(["abc", None], dtype=ArrowDtype(pa.string()))
    with pytest.raises(NotImplementedError, match="count not"):
        ser.str.count("abc", flags=1)

