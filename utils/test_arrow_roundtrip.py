
def test_arrow_roundtrip(data):
    df = pd.DataFrame({"a": data})
    table = pa.table(df)
    assert table.field("a").type == str(data.dtype.numpy_dtype)

    result = table.to_pandas()
    assert result["a"].dtype == data.dtype
    tm.assert_frame_equal(result, df)


def test_arrow_roundtrip(dtype, string_storage, using_infer_string):
    # roundtrip possible from arrow 1.0.0
    pa = pytest.importorskip("pyarrow")

    data = pd.array(["a", "b", None], dtype=dtype)
    df = pd.DataFrame({"a": data})
    table = pa.table(df)
    if dtype.storage == "python":
        assert table.field("a").type == "string"
    else:
        assert table.field("a").type == "large_string"
    with pd.option_context("string_storage", string_storage):
        result = table.to_pandas()

    assert isinstance(result["a"].dtype, pd.StringDtype)
    expected = df.astype(pd.StringDtype(string_storage, na_value=dtype.na_value))
    if using_infer_string:
        expected.columns = expected.columns.astype(
            pd.StringDtype(string_storage, na_value=np.nan)
        )
    tm.assert_frame_equal(result, expected)
    # ensure the missing value is represented by NA and not np.nan or None
    assert result.loc[2, "a"] is result["a"].dtype.na_value

