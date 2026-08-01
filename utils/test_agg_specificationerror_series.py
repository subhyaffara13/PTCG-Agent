
def test_agg_specificationerror_series(cases, agg):
    msg = "nested renamer is not supported"

    # series like aggs
    with pytest.raises(pd.errors.SpecificationError, match=msg):
        cases["A"].agg(agg)

