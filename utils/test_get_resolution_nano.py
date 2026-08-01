
def test_get_resolution_nano():
    # don't return the fallback RESO_DAY
    arr = np.array([1], dtype=np.int64)
    res = get_resolution(arr)
    assert res == Resolution.RESO_NS

