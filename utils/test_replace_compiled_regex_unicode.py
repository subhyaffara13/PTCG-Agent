import re

def test_replace_compiled_regex_unicode(any_string_dtype):
    ser = Series([b"abcd,\xc3\xa0".decode("utf-8")], dtype=any_string_dtype)
    expected = Series([b"abcd, \xc3\xa0".decode("utf-8")], dtype=any_string_dtype)
    pat = re.compile(r"(?<=\w),(?=\w)", flags=re.UNICODE)
    result = ser.str.replace(pat, ", ", regex=True)
    tm.assert_series_equal(result, expected)

