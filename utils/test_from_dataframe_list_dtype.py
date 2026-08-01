
def test_from_dataframe_list_dtype():
    pa = pytest.importorskip("pyarrow", "14.0.0")
    data = {"a": [[1, 2], [4, 5, 6]]}
    tbl = pa.table(data)
    result = from_dataframe(tbl)
    expected = pd.DataFrame(data)
    tm.assert_frame_equal(result, expected)

