
def test_pandas_dtype_ea_not_instance():
    # GH 31356 GH 54592
    with tm.assert_produces_warning(UserWarning, match="without any arguments"):
        assert pandas_dtype(CategoricalDtype) == CategoricalDtype()

