
def test_getitem_non_found_tuple():
    # GH: 25236
    df = DataFrame([[1, 2, 3, 4]], columns=["a", "b", "c", "d"]).set_index(
        ["a", "b", "c"]
    )
    with pytest.raises(KeyError, match=r"\(2\.0, 2\.0, 3\.0\)"):
        df.loc[(2.0, 2.0, 3.0)]

