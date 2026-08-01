
def test_groups_repr_truncates(max_seq_items, expected):
    # GH 1135
    df = DataFrame(np.random.default_rng(2).standard_normal((5, 1)))
    df["a"] = df.index

    with pd.option_context("display.max_seq_items", max_seq_items):
        result = df.groupby("a").groups.__repr__()
        assert result == expected

        result = df.groupby(np.array(df.a)).groups.__repr__()
        assert result == expected

