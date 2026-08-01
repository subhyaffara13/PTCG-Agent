
def test_pandas_warnings_filter(warn_category, filter_category):
    # https://github.com/pandas-dev/pandas/pull/61468
    # Ensure users can suppress warnings.
    with tm.assert_produces_warning(None), warnings.catch_warnings():
        warnings.filterwarnings(category=filter_category, action="ignore")
        warnings.warn("test", category=warn_category)

