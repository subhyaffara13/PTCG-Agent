import re

def test_read_nokey_empty(temp_h5_path):
    store = HDFStore(temp_h5_path)
    store.close()
    msg = re.escape(
        "Dataset(s) incompatible with Pandas data types, not table, or no "
        "datasets found in HDF5 file."
    )
    with pytest.raises(ValueError, match=msg):
        read_hdf(temp_h5_path)

