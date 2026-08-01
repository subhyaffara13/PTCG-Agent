
def test_infer_string_columns(temp_h5_path):
    # GH#
    pytest.importorskip("pyarrow")
    with pd.option_context("future.infer_string", True):
        df = DataFrame(1, columns=list("ABCD"), index=list(range(10))).set_index(
            ["A", "B"]
        )
        expected = df.copy()
        df.to_hdf(temp_h5_path, key="df", format="table")

        result = read_hdf(temp_h5_path, "df")
        tm.assert_frame_equal(result, expected)

