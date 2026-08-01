
def test_invalid_new_style_format_missing_brace():
    df = DataFrame({"A": [1.23]})
    with pytest.raises(ValueError, match="Invalid new-style format string '{:.2f"):
        df.to_csv(float_format="{:.2f")

