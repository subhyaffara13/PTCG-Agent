
def test_pytables_native2_read(datapath):
    with HDFStore(
        datapath("io", "data", "legacy_hdf", "pytables_native2.h5"), mode="r"
    ) as store:
        str(store)
        d1 = store["detector"]
    assert isinstance(d1, DataFrame)

