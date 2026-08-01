
def test_arrow_table_roundtrip_without_metadata(breaks):
    pa = pytest.importorskip("pyarrow")

    arr = IntervalArray.from_breaks(breaks)
    arr[1] = None
    df = pd.DataFrame({"a": arr})

    table = pa.table(df)
    # remove the metadata
    table = table.replace_schema_metadata()
    assert table.schema.metadata is None

    result = table.to_pandas()
    assert isinstance(result["a"].dtype, pd.IntervalDtype)
    tm.assert_frame_equal(result, df)


def test_arrow_table_roundtrip_without_metadata():
    arr = PeriodArray([1, 2, 3], dtype="period[h]")
    arr[1] = pd.NaT
    df = pd.DataFrame({"a": arr})

    table = pa.table(df)
    # remove the metadata
    table = table.replace_schema_metadata()
    assert table.schema.metadata is None

    result = table.to_pandas()
    assert isinstance(result["a"].dtype, PeriodDtype)
    tm.assert_frame_equal(result, df)

