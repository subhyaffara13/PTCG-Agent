
def test_invalid_float_format_type():
    df = DataFrame({"A": [1.23]})
    with pytest.raises(ValueError, match="float_format must be a string or callable"):
        df.to_csv(float_format=123)

