
def test_copy_deprecation_merge_concat():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    with tm.assert_produces_warning(
        Pandas4Warning, match="copy", check_stacklevel=False
    ):
        df.merge(df, copy=False)

    with tm.assert_produces_warning(
        Pandas4Warning, match="copy", check_stacklevel=False
    ):
        merge(df, df, copy=False)

    with tm.assert_produces_warning(
        Pandas4Warning, match="copy", check_stacklevel=False
    ):
        concat([df, df], copy=False)

