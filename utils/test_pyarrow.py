
def test_pyarrow(df):
    pyarrow = pytest.importorskip("pyarrow")
    table = pyarrow.Table.from_pandas(df)
    result = table.to_pandas()
    tm.assert_frame_equal(result, df)

