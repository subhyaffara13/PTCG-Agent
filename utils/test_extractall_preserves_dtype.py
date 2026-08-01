
def test_extractall_preserves_dtype():
    # Ensure that when extractall is called on a series with specific dtypes set, that
    # the dtype is preserved in the resulting DataFrame's column.
    pa = pytest.importorskip("pyarrow")

    result = Series(["abc", "ab"], dtype=ArrowDtype(pa.string())).str.extractall("(ab)")
    assert result.dtypes[0] == "string[pyarrow]"

