
def test_findall(example_source):
    found = list(setuptools.findall(str(example_source)))
    expected = ['readme.txt', 'foo/bar.py']
    expected = [example_source.join(fn) for fn in expected]
    assert found == expected


def test_findall(any_string_dtype):
    ser = Series(["fooBAD__barBAD", np.nan, "foo", "BAD"], dtype=any_string_dtype)
    result = ser.str.findall("BAD[_]*")
    expected = Series([["BAD__", "BAD"], np.nan, [], ["BAD"]])
    expected = _convert_na_value(ser, expected)
    tm.assert_series_equal(result, expected)

