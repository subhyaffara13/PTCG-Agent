
def test_arrow_load_from_zero_chunks(data):
    # GH-41040

    df = pd.DataFrame({"a": data[0:0]})
    table = pa.table(df)
    assert table.field("a").type == str(data.dtype.numpy_dtype)
    table = pa.table(
        [pa.chunked_array([], type=table.field("a").type)], schema=table.schema
    )
    result = table.to_pandas()
    assert result["a"].dtype == data.dtype
    tm.assert_frame_equal(result, df)


def test_arrow_load_from_zero_chunks():
    # GH-41040

    from pandas.core.arrays.arrow.extension_types import ArrowPeriodType

    arr = PeriodArray([], dtype="period[D]")
    df = pd.DataFrame({"a": arr})

    table = pa.table(df)
    assert isinstance(table.field("a").type, ArrowPeriodType)
    table = pa.table(
        [pa.chunked_array([], type=table.column(0).type)], schema=table.schema
    )

    result = table.to_pandas()
    assert isinstance(result["a"].dtype, PeriodDtype)
    tm.assert_frame_equal(result, df)


def test_arrow_load_from_zero_chunks(dtype, string_storage, using_infer_string):
    # GH-41040
    pa = pytest.importorskip("pyarrow")

    data = pd.array([], dtype=dtype)
    df = pd.DataFrame({"a": data})
    table = pa.table(df)
    if dtype.storage == "python":
        assert table.field("a").type == "string"
    else:
        assert table.field("a").type == "large_string"
    # Instantiate the same table with no chunks at all
    table = pa.table([pa.chunked_array([], type=pa.string())], schema=table.schema)
    with pd.option_context("string_storage", string_storage):
        result = table.to_pandas()

    assert isinstance(result["a"].dtype, pd.StringDtype)
    expected = df.astype(pd.StringDtype(string_storage, na_value=dtype.na_value))
    if using_infer_string:
        expected.columns = expected.columns.astype(
            pd.StringDtype(string_storage, na_value=np.nan)
        )
    tm.assert_frame_equal(result, expected)

