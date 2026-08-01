
def test_retain_datetime_attribute(temp_h5_path):
    ser = Series(
        ["2024-08-26 15:13:14", "2024-08-26 15:14:14"],
        dtype="datetime64[us, UTC]",
    )
    dataframe = DataFrame(ser)
    dataframe.to_hdf(temp_h5_path, key="Annotations", mode="w")

    recovered_dataframe = read_hdf(temp_h5_path, key="Annotations")
    tm.assert_frame_equal(dataframe, recovered_dataframe)

