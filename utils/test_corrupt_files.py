
def test_corrupt_files():
    # Test we can detect truncated or corrupt (all zero) files.
    for n in (2, 4, 10, 19):
        with pytest.raises(MatReadError,
                           match="Mat file appears to be truncated"):
            loadmat(BytesIO(b'\x00' * n))
    with pytest.raises(MatReadError,
                       match="Mat file appears to be corrupt"):
        loadmat(BytesIO(b'\x00' * 20))

