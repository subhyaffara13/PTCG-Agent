
def test_drop_not_lexsorted(performance_warning):
    # GH 12078

    # define the lexsorted version of the multi-index
    tuples = [("a", ""), ("b1", "c1"), ("b2", "c2")]
    lexsorted_mi = MultiIndex.from_tuples(tuples, names=["b", "c"])
    assert lexsorted_mi._is_lexsorted()

    # and the not-lexsorted version
    df = pd.DataFrame(
        columns=["a", "b", "c", "d"], data=[[1, "b1", "c1", 3], [1, "b2", "c2", 4]]
    )
    df = df.pivot_table(index="a", columns=["b", "c"], values="d")
    df = df.reset_index()
    not_lexsorted_mi = df.columns
    assert not not_lexsorted_mi._is_lexsorted()

    # compare the results
    tm.assert_index_equal(lexsorted_mi, not_lexsorted_mi)
    with tm.assert_produces_warning(performance_warning):
        tm.assert_index_equal(lexsorted_mi.drop("a"), not_lexsorted_mi.drop("a"))

