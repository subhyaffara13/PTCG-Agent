
def test_str_extract_non_symbolic():
    ser = pd.Series(["a1", "b2", "c3"], dtype=ArrowDtype(pa.string()))
    with pytest.raises(ValueError, match="pat=.* must contain a symbolic group name."):
        ser.str.extract(r"[ab](\d)")

