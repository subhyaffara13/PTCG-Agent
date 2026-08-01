
def test_agg_specificationerror_invalid_names(cases):
    # errors
    # invalid names in the agg specification
    msg = r"Label\(s\) \['B'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        cases[["A"]].agg({"A": ["sum", "std"], "B": ["mean", "std"]})

