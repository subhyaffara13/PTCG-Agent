
def test_implicit_casting():
    """Tests implicit casting when assigning or appending to dicts and lists."""
    z = m.get_implicit_casting()
    assert z["d"] == {
        "char*_i1": "abc",
        "char*_i2": "abc",
        "char*_e": "abc",
        "char*_p": "abc",
        "str_i1": "str",
        "str_i2": "str1",
        "str_e": "str2",
        "str_p": "str3",
        "int_i1": 42,
        "int_i2": 42,
        "int_e": 43,
        "int_p": 44,
    }
    assert z["l"] == [3, 6, 9, 12, 15]

