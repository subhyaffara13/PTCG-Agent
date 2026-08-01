
def test_to_numpy_na_raises(box, dtype):
    con = pd.Series if box else pd.array
    arr = con([0.0, 1.0, None], dtype="Float64")
    with pytest.raises(ValueError, match=dtype):
        arr.to_numpy(dtype=dtype)


def test_to_numpy_na_raises(dtype):
    a = pd.array([0, 1, None], dtype="Int64")
    with pytest.raises(ValueError, match=dtype):
        a.to_numpy(dtype=dtype)

