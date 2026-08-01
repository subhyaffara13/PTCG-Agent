
def test_dict_nested_renaming_depr(method):
    df = DataFrame({"A": range(5), "B": 5})

    # nested renaming
    msg = r"nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        getattr(df, method)({"A": {"foo": "min"}, "B": {"bar": "max"}})

