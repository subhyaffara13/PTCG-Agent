
def test_unsuppored_hdf_file_error(datapath):
    # GH 9539
    data_path = datapath("io", "data", "legacy_hdf/incompatible_dataset.h5")
    message = (
        r"Dataset\(s\) incompatible with Pandas data types, "
        "not table, or no datasets found in HDF5 file."
    )

    with pytest.raises(ValueError, match=message):
        read_hdf(data_path)

