
def test_null_roundtripping():
    data = ["hello\0world", "ABC\0DEF\0\0"]
    arr = np.array(data, dtype="T")
    assert data[0] == arr[0]
    assert data[1] == arr[1]

