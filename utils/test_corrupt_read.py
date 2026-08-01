
def test_corrupt_read(datapath):
    # We don't really care about the exact failure, the important thing is
    # that the resource should be cleaned up afterwards (BUG #35566)
    fname = datapath("io", "sas", "data", "corrupt.sas7bdat")
    msg = "'SAS7BDATReader' object has no attribute 'row_count'"
    with pytest.raises(AttributeError, match=msg):
        pd.read_sas(fname)

