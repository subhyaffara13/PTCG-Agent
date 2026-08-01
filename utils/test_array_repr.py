
def test_array_repr(any_numpy_array):
    # GH#61085
    nparray = any_numpy_array
    arr = NumpyExtensionArray(nparray)
    if nparray.dtype == "object":
        values = "['a', 'b']"
    elif nparray.dtype == "float64":
        values = "[0.0, 1.0]"
    elif str(nparray.dtype).startswith("int"):
        values = "[0, 1]"
    elif nparray.dtype == "complex128":
        values = "[0j, (1+2j)]"
    elif nparray.dtype == "bool":
        values = "[True, False]"
    elif nparray.dtype == "datetime64[ns]":
        values = "[1970-01-01T00:00:00.000000000, 1970-01-01T00:00:00.000000001]"
    elif nparray.dtype == "timedelta64[ns]":
        values = "[0 nanoseconds, 1 nanoseconds]"
    expected = f"<NumpyExtensionArray>\n{values}\nLength: 2, dtype: {nparray.dtype}"
    result = repr(arr)
    assert result == expected, f"{result} vs {expected}"


def test_array_repr():
    o = 1 + LD_INFO.eps
    a = np.array([o])
    b = np.array([1], dtype=np.longdouble)
    if not np.all(a != b):
        raise ValueError("precision loss creating arrays")
    with np.printoptions(precision=LD_INFO.precision + 1):
        assert_(repr(a) != repr(b))

