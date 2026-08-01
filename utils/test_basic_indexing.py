
def test_basic_indexing():
    s = Series(
        np.random.default_rng(2).standard_normal(5), index=["a", "b", "a", "a", "b"]
    )

    with pytest.raises(KeyError, match="^5$"):
        s[5]

    with pytest.raises(KeyError, match=r"^'c'$"):
        s["c"]

    s = s.sort_index()

    with pytest.raises(KeyError, match="^5$"):
        s[5]

