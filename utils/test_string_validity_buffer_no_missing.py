
def test_string_validity_buffer_no_missing() -> None:
    # https://github.com/pandas-dev/pandas/issues/57762
    pytest.importorskip("pyarrow", "11.0.0")
    df = pd.DataFrame({"a": ["x", None]}, dtype="large_string[pyarrow]")
    with tm.assert_produces_warning(match="Interchange"):
        validity = df.__dataframe__().get_column_by_name("a").get_buffers()["validity"]
    assert validity is not None
    result = validity[1]
    expected = (DtypeKind.BOOL, 1, ArrowCTypes.BOOL, "=")
    assert result == expected

