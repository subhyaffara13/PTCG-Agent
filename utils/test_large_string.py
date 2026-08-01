
def test_large_string():
    # GH#56702
    pytest.importorskip("pyarrow")
    df = pd.DataFrame({"a": ["x"]}, dtype="large_string[pyarrow]")
    # Don't check stacklevel as PyArrow calls the deprecated `__dataframe__` method.
    with tm.assert_produces_warning(match="Interchange", check_stacklevel=False):
        result = pd.api.interchange.from_dataframe(df.__dataframe__())
    expected = pd.DataFrame({"a": ["x"]}, dtype="str")
    tm.assert_frame_equal(result, expected)

