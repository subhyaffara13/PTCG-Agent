
def test_unsupported_mode(mode):
    match = f"mode '{mode}' is not supported"
    with pytest.raises(ValueError, match=match):
        np.pad([1, 2, 3], 4, mode=mode)

