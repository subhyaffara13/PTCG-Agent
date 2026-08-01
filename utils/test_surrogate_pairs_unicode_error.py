
def test_surrogate_pairs_unicode_error(func):
    input_str = "\ud83d\ude4f".encode("utf-8", "surrogatepass")
    with pytest.raises(UnicodeDecodeError):
        func(input_str)

