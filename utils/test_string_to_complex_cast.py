
def test_string_to_complex_cast(str_type, scalar_type):
    value = scalar_type(b"1+3j")
    assert scalar_type(value) == 1 + 3j
    assert np.array([value], dtype=object).astype(scalar_type)[()] == 1 + 3j
    assert np.array(value).astype(scalar_type)[()] == 1 + 3j
    arr = np.zeros(1, dtype=scalar_type)
    arr[0] = value
    assert arr[0] == 1 + 3j

