
def test_nan_in_xls(datapath):
    # GH 54564
    path = datapath("io", "data", "excel", "test6.xls")

    expected = pd.DataFrame({0: np.r_[0, 2].astype("int64"), 1: np.r_[1, np.nan]})

    result = pd.read_excel(path, header=None)

    tm.assert_frame_equal(result, expected)

