
def test_agg_dict_renaming_deprecation():
    # 15931
    df = DataFrame({"A": [1, 1, 1, 2, 2], "B": range(5), "C": range(5)})

    msg = r"nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        df.groupby("A").agg(
            {"B": {"foo": ["sum", "max"]}, "C": {"bar": ["count", "min"]}}
        )

    msg = r"Label\(s\) \['ma'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        df.groupby("A")[["B", "C"]].agg({"ma": "max"})

    msg = r"nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        df.groupby("A").B.agg({"foo": "count"})

