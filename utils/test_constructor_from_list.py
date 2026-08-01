
def test_constructor_from_list():
    # GH#27673
    pytest.importorskip("pyarrow")
    result = pd.Series(["E"], dtype=StringDtype(storage="pyarrow"))
    assert isinstance(result.dtype, StringDtype)
    assert result.dtype.storage == "pyarrow"

