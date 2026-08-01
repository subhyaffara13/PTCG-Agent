
def test_concatenate_chunks_pyarrow_strings():
    # GH#51876
    pa = pytest.importorskip("pyarrow")
    chunks = [
        {0: ArrowExtensionArray(pa.array([1.5, 2.5]))},
        {0: ArrowExtensionArray(pa.array(["a", "b"]))},
    ]
    with tm.assert_produces_warning(
        DtypeWarning, match="Columns \\(0: column_0\\) have mixed types"
    ):
        result = _concatenate_chunks(chunks, ["column_0", "column_1"])
    expected = np.concatenate(
        [np.array([1.5, 2.5], dtype=object), np.array(["a", "b"])]
    )
    tm.assert_numpy_array_equal(result[0], expected)

