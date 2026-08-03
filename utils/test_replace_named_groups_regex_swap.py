import re

def test_replace_named_groups_regex_swap(
    any_string_dtype, use_compile, repl, expected_list
):
    # GH#57636
    ser = Series(["One Two Three", "Foo Bar Baz"], dtype=any_string_dtype)
    pattern = r"(?P<one>\w+) (?P<two>\w+) (?P<three>\w+)"
    if use_compile:
        pattern = re.compile(pattern)
    result = ser.str.replace(pattern, repl, regex=True)
    expected = Series(expected_list, dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

