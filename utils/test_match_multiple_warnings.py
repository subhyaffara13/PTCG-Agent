
def test_match_multiple_warnings():
    # https://github.com/pandas-dev/pandas/issues/47829
    category = (FutureWarning, UserWarning)
    with tm.assert_produces_warning(category, match=r"^Match this"):
        warnings.warn("Match this", FutureWarning)  # pdlint: ignore[warning_class]
        warnings.warn("Match this too", UserWarning)

