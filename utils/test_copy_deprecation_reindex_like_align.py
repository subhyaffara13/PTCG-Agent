
def test_copy_deprecation_reindex_like_align():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    # Somehow the stack level check is incorrect here
    with tm.assert_produces_warning(
        Pandas4Warning, match="copy", check_stacklevel=False
    ):
        df.reindex_like(df, copy=False)

    with tm.assert_produces_warning(
        Pandas4Warning, match="copy", check_stacklevel=False
    ):
        df.a.reindex_like(df.a, copy=False)

    with tm.assert_produces_warning(
        Pandas4Warning, match="copy", check_stacklevel=False
    ):
        df.align(df, copy=False)

    with tm.assert_produces_warning(
        Pandas4Warning, match="copy", check_stacklevel=False
    ):
        df.a.align(df.a, copy=False)

