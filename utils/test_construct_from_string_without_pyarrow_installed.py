
def test_construct_from_string_without_pyarrow_installed():
    # GH 57928
    with pytest.raises(ImportError, match="pyarrow>=.* is required"):
        pd.Series([-1.5, 0.2, None], dtype="float32[pyarrow]")

