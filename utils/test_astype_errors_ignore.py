
def test_astype_errors_ignore():
    # GH 55399
    expected = pd.DataFrame({"col": [17000000]}, dtype="int32[pyarrow]")
    result = expected.astype("float[pyarrow]", errors="ignore")
    tm.assert_frame_equal(result, expected)

