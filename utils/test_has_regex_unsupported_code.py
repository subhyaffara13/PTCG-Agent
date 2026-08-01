
def test_has_regex_unsupported_code(pat, expected):
    # https://github.com/pandas-dev/pandas/issues/60833
    assert ArrowStringArrayMixin._has_unsupported_regex(pat) == expected

