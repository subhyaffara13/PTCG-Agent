
def test_void_via_length(length):
    res = np.void(length)
    assert type(res) is np.void
    assert res.item() == b"\0" * 5
    assert res.dtype == "V5"

