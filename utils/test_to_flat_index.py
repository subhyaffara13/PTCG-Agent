
def test_to_flat_index(idx):
    expected = pd.Index(
        (
            ("foo", "one"),
            ("foo", "two"),
            ("bar", "one"),
            ("baz", "two"),
            ("qux", "one"),
            ("qux", "two"),
        ),
        tupleize_cols=False,
    )
    result = idx.to_flat_index()
    tm.assert_index_equal(result, expected)

