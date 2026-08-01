
def test_pandas_nullable_without_missing_values(
    data: list, dtype: str, expected_dtype: str
) -> None:
    # https://github.com/pandas-dev/pandas/issues/57643
    pa = pytest.importorskip("pyarrow", "14.0.0")
    import pyarrow.interchange as pai

    if expected_dtype == "timestamp[us, tz=Asia/Kathmandu]":
        expected_dtype = pa.timestamp("us", "Asia/Kathmandu")

    df = pd.DataFrame({"a": data}, dtype=dtype)
    with tm.assert_produces_warning(match="Interchange"):
        result = pai.from_dataframe(df.__dataframe__())["a"]
    assert result.type == expected_dtype
    assert result[0].as_py() == data[0]
    assert result[1].as_py() == data[1]
    assert result[2].as_py() == data[2]

