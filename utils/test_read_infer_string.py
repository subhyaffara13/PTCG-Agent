
def test_read_infer_string(temp_h5_path):
    # GH#54431
    df = DataFrame({"a": ["a", "b", None]})
    df.to_hdf(temp_h5_path, key="data", format="table")
    with pd.option_context("future.infer_string", True):
        result = read_hdf(temp_h5_path, key="data", mode="r")
    expected = DataFrame(
        {"a": ["a", "b", None]},
        dtype=pd.StringDtype(na_value=np.nan),
        columns=Index(["a"], dtype=pd.StringDtype(na_value=np.nan)),
    )
    tm.assert_frame_equal(result, expected)

