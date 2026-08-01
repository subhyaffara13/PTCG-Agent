
def test_allow_partial_match_for_multiple_warnings_messages():
    # https://github.com/pandas-dev/pandas/issues/56555
    category = (FutureWarning, UserWarning)
    with tm.assert_produces_warning(
        category, match=r"^Match this", must_find_all_warnings=False
    ):
        warnings.warn("Match this", FutureWarning)  # pdlint: ignore[warning_class]
        warnings.warn("Not this", UserWarning)

