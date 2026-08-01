
def test_must_match_multiple_warnings_messages():
    # https://github.com/pandas-dev/pandas/issues/56555
    category = (FutureWarning, UserWarning)
    msg = r"The emitted warning messages are \[UserWarning\('Not this'\)\]"
    with pytest.raises(AssertionError, match=msg):
        with tm.assert_produces_warning(category, match=r"^Match this"):
            warnings.warn("Match this", FutureWarning)  # pdlint: ignore[warning_class]
            warnings.warn("Not this", UserWarning)

