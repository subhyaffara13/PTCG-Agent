
def test_series_arrow_interface_stringdtype():
    s = pd.Series(["foo", "bar"], dtype="string[pyarrow]")

    capsule = s.__arrow_c_stream__()
    assert (
        ctypes.pythonapi.PyCapsule_IsValid(
            ctypes.py_object(capsule), b"arrow_array_stream"
        )
        == 1
    )

    ca = pa.chunked_array(s)
    expected = pa.chunked_array([["foo", "bar"]], type=pa.large_string())
    assert ca.equals(expected)

