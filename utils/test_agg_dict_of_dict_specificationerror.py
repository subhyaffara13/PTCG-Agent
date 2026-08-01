
def test_agg_dict_of_dict_specificationerror(cases, agg):
    msg = "nested renamer is not supported"
    with pytest.raises(pd.errors.SpecificationError, match=msg):
        cases.aggregate(agg)

