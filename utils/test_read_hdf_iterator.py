
def test_read_hdf_iterator(temp_h5_path):
    df = DataFrame(
        np.random.default_rng(2).random((4, 5)),
        index=list("abcd"),
        columns=list("ABCDE"),
    )
    df.index.name = "letters"
    df = df.set_index(keys="E", append=True)

    df.to_hdf(temp_h5_path, key="df", mode="w", format="t")
    direct = read_hdf(temp_h5_path, "df")
    iterator = read_hdf(temp_h5_path, "df", iterator=True)
    with closing(iterator.store):
        assert isinstance(iterator, TableIterator)
        indirect = next(iterator.__iter__())
    tm.assert_frame_equal(direct, indirect)

