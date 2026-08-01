
def test_invalid_terms_reference(temp_h5_path):
    # catch the invalid reference
    dfq = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=list("ABCD"),
        index=date_range("20130101", periods=10, unit="ns"),
    )
    dfq.to_hdf(temp_h5_path, key="dfq", format="table")

    msg = (
        r"The passed where expression: A>0 or C>0\n\s*"
        r"contains an invalid variable reference\n\s*"
        r"all of the variable references must be a reference to\n\s*"
        r"an axis \(e.g. 'index' or 'columns'\), or a data_column\n\s*"
        r"The currently defined references are: index,columns\n"
    )
    with pytest.raises(ValueError, match=msg):
        read_hdf(temp_h5_path, "dfq", where="A>0 or C>0")

