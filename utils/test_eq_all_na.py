
def test_eq_all_na():
    pytest.importorskip("pyarrow")
    a = pd.array([NA, NA], dtype=StringDtype("pyarrow"))
    result = a == a
    expected = pd.array([NA, NA], dtype="boolean[pyarrow]")
    tm.assert_extension_array_equal(result, expected)

