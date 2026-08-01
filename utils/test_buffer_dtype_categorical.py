
def test_buffer_dtype_categorical(
    data: pd.Series,
    expected_dtype: tuple[DtypeKind, int, str, str],
    expected_buffer_dtype: tuple[DtypeKind, int, str, str],
) -> None:
    # https://github.com/pandas-dev/pandas/issues/54781
    df = pd.DataFrame({"data": data})
    with tm.assert_produces_warning(match="Interchange"):
        dfi = df.__dataframe__()
    col = dfi.get_column_by_name("data")
    assert col.dtype == expected_dtype
    assert col.get_buffers()["data"][1] == expected_buffer_dtype

