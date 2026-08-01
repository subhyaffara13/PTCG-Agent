
def test_columns_multiindex_modified(temp_h5_path):
    # BUG: 7212

    df = DataFrame(
        np.random.default_rng(2).random((4, 5)),
        index=list("abcd"),
        columns=list("ABCDE"),
    )
    df.index.name = "letters"
    df = df.set_index(keys="E", append=True)

    data_columns = df.index.names + df.columns.tolist()
    df.to_hdf(
        temp_h5_path,
        key="df",
        mode="a",
        append=True,
        data_columns=data_columns,
        index=False,
    )
    cols2load = list("BCD")
    cols2load_original = list(cols2load)
    # GH#10055 make sure read_hdf call does not alter cols2load inplace
    read_hdf(temp_h5_path, "df", columns=cols2load)
    assert cols2load_original == cols2load

