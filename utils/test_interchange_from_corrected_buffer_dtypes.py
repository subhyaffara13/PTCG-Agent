
def test_interchange_from_corrected_buffer_dtypes(monkeypatch) -> None:
    # https://github.com/pandas-dev/pandas/issues/54781
    with tm.assert_produces_warning(match="Interchange"):
        df = pd.DataFrame({"a": ["foo", "bar"]}).__dataframe__()
        interchange = df.__dataframe__()
    column = interchange.get_column_by_name("a")
    buffers = column.get_buffers()
    buffers_data = buffers["data"]
    buffer_dtype = buffers_data[1]
    buffer_dtype = (
        DtypeKind.UINT,
        8,
        ArrowCTypes.UINT8,
        buffer_dtype[3],
    )
    buffers["data"] = (buffers_data[0], buffer_dtype)
    column.get_buffers = lambda: buffers
    interchange.get_column_by_name = lambda _: column
    monkeypatch.setattr(df, "__dataframe__", lambda allow_copy: interchange)
    with tm.assert_produces_warning(match="Interchange"):
        pd.api.interchange.from_dataframe(df)

