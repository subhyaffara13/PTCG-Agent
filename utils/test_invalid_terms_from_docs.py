
def test_invalid_terms_from_docs(temp_h5_path):
    # from the docs
    dfq = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=list("ABCD"),
        index=date_range("20130101", periods=10, unit="ns"),
    )
    dfq.to_hdf(temp_h5_path, key="dfq", format="table", data_columns=True)

    # check ok
    read_hdf(
        temp_h5_path, "dfq", where="index>Timestamp('20130104') & columns=['A', 'B']"
    )
    read_hdf(temp_h5_path, "dfq", where="A>0 or C>0")

