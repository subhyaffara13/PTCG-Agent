
def test_void_from_byteslike(bytes_):
    res = np.void(bytes_)
    expected = bytes(bytes_)
    assert type(res) is np.void
    assert res.item() == expected

    # Passing dtype can extend it (this is how filling works)
    res = np.void(bytes_, dtype="V100")
    assert type(res) is np.void
    assert res.item()[:len(expected)] == expected
    assert res.item()[len(expected):] == b"\0" * (res.nbytes - len(expected))
    # As well as shorten:
    res = np.void(bytes_, dtype="V4")
    assert type(res) is np.void
    assert res.item() == expected[:4]

