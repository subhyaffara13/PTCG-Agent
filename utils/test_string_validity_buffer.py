
def test_string_validity_buffer() -> None:
    # https://github.com/pandas-dev/pandas/issues/57761
    pytest.importorskip("pyarrow", "11.0.0")
    df = pd.DataFrame({"a": ["x"]}, dtype="large_string[pyarrow]")
    with tm.assert_produces_warning(match="Interchange"):
        result = df.__dataframe__().get_column_by_name("a").get_buffers()["validity"]
    assert result is None

