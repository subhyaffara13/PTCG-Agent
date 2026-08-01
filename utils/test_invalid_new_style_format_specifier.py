
def test_invalid_new_style_format_specifier():
    df = DataFrame({"A": [1.23]})
    with pytest.raises(ValueError, match="Invalid new-style format string '{:.2z}'"):
        df.to_csv(float_format="{:.2z}")

