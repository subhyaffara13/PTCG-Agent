
def test_encoding_errors_badtype(encoding_errors):
    # GH 59075
    content = StringIO("A,B\n1,2\n3,4\n")
    reader = partial(pd.read_csv, encoding_errors=encoding_errors)
    expected_error = "encoding_errors must be a string, got "
    expected_error += f"{type(encoding_errors).__name__}"
    with pytest.raises(ValueError, match=expected_error):
        reader(content)

