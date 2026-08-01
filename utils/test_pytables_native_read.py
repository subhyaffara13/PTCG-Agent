
def test_pytables_native_read(datapath):
    with HDFStore(
        datapath("io", "data", "legacy_hdf/pytables_native.h5"), mode="r"
    ) as store:
        d2 = store["detector/readout"]
    assert isinstance(d2, DataFrame)

