
def test_read_csv_chained_url_no_error(datapath, compression):
    # GH 60100
    tar_file_path = datapath("io", "data", "tar", "test-csv.tar")
    chained_file_url = f"tar://test.csv::file://{tar_file_path}"

    result = pd.read_csv(chained_file_url, compression=compression, sep=";")
    expected = pd.DataFrame({"1": {0: 3}, "2": {0: 4}})

    tm.assert_frame_equal(expected, result)

