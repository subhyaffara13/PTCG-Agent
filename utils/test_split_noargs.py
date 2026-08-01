
def test_split_noargs(any_string_dtype, method):
    # #1859
    s = Series(["Wes McKinney", "Travis  Oliphant"], dtype=any_string_dtype)
    result = getattr(s.str, method)()
    expected = ["Travis", "Oliphant"]
    assert result[1] == expected

