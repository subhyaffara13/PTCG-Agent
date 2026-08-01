
def test_concatenate_chunks_pyarrow():
    # GH#51876
    pa = pytest.importorskip("pyarrow")
    chunks = [
        {0: ArrowExtensionArray(pa.array([1.5, 2.5]))},
        {0: ArrowExtensionArray(pa.array([1, 2]))},
    ]
    result = _concatenate_chunks(chunks, ["column_0", "column_1"])
    expected = ArrowExtensionArray(pa.array([1.5, 2.5, 1.0, 2.0]))
    tm.assert_extension_array_equal(result[0], expected)

