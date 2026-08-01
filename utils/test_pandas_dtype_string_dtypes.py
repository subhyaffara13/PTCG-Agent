
def test_pandas_dtype_string_dtypes(string_storage):
    with pd.option_context("future.infer_string", True):
        # with the default string_storage setting
        result = pandas_dtype("str")
    assert result == pd.StringDtype(
        "pyarrow" if HAS_PYARROW else "python", na_value=np.nan
    )

    with pd.option_context("future.infer_string", True):
        # with the default string_storage setting
        result = pandas_dtype(str)
    assert result == pd.StringDtype(
        "pyarrow" if HAS_PYARROW else "python", na_value=np.nan
    )

    with pd.option_context("future.infer_string", True):
        with pd.option_context("string_storage", string_storage):
            result = pandas_dtype("str")
    assert result == pd.StringDtype(string_storage, na_value=np.nan)

    with pd.option_context("future.infer_string", True):
        with pd.option_context("string_storage", string_storage):
            result = pandas_dtype(str)
    assert result == pd.StringDtype(string_storage, na_value=np.nan)

    with pd.option_context("future.infer_string", False):
        with pd.option_context("string_storage", string_storage):
            result = pandas_dtype("str")
    assert result == np.dtype("U")

    with pd.option_context("string_storage", string_storage):
        result = pandas_dtype("string")
    assert result == pd.StringDtype(string_storage, na_value=pd.NA)

