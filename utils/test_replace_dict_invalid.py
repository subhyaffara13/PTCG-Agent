
def test_replace_dict_invalid(any_string_dtype):
    # GH 51914
    series = Series(data=["A", "B_junk", "C_gunk"], name="my_messy_col")
    msg = "repl cannot be used when pat is a dictionary"

    with pytest.raises(ValueError, match=msg):
        series.str.replace(pat={"A": "a", "B": "b"}, repl="A")

