
def test_dtype_repr(dtype):
    if dtype.storage == "pyarrow":
        if dtype.na_value is pd.NA:
            assert repr(dtype) == "<StringDtype(na_value=<NA>)>"
        else:
            assert repr(dtype) == "<StringDtype(na_value=nan)>"
    elif dtype.na_value is pd.NA:
        assert repr(dtype) == "<StringDtype(storage='python', na_value=<NA>)>"
    else:
        assert repr(dtype) == "<StringDtype(storage='python', na_value=nan)>"


def test_dtype_repr(dtype):
    if not hasattr(dtype, "na_object") and dtype.coerce:
        assert repr(dtype) == "StringDType()"
    elif dtype.coerce:
        assert repr(dtype) == f"StringDType(na_object={dtype.na_object!r})"
    elif not hasattr(dtype, "na_object"):
        assert repr(dtype) == "StringDType(coerce=False)"
    else:
        assert (
            repr(dtype)
            == f"StringDType(na_object={dtype.na_object!r}, coerce=False)"
        )

