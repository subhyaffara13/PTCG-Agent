
def test_pandas_warnings(warn_category, catch_category):
    # https://github.com/pandas-dev/pandas/pull/61468
    with tm.assert_produces_warning(catch_category):
        warnings.warn("test", category=warn_category)

