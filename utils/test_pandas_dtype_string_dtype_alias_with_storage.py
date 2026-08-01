
def test_pandas_dtype_string_dtype_alias_with_storage():
    with pytest.raises(TypeError, match="not understood"):
        pandas_dtype("str[python]")

    with pytest.raises(TypeError, match="not understood"):
        pandas_dtype("str[pyarrow]")

    result = pandas_dtype("string[python]")
    assert result == pd.StringDtype("python", na_value=pd.NA)

    if HAS_PYARROW:
        result = pandas_dtype("string[pyarrow]")
        assert result == pd.StringDtype("pyarrow", na_value=pd.NA)
    else:
        with pytest.raises(
            ImportError, match="required for PyArrow backed StringArray"
        ):
            pandas_dtype("string[pyarrow]")

