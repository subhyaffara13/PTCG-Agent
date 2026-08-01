
def test_array_astype_to_void(dt):
    dt = np.dtype(dt)
    arr = np.array([], dtype=dt)
    assert arr.astype("V").dtype.itemsize == dt.itemsize

