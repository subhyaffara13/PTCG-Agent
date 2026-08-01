
def test_multi_norm_call_vmin_vmax():
    # test get vmin, vmax
    norm = mpl.colors.MultiNorm(['linear', 'log'])
    norm.vmin = (1, 1)
    norm.vmax = (2, 2)
    assert norm.vmin == (1, 1)
    assert norm.vmax == (2, 2)

    with pytest.raises(ValueError, match="Expected an iterable of length 2"):
        norm.vmin = 1
    with pytest.raises(ValueError, match="Expected an iterable of length 2"):
        norm.vmax = 1
    with pytest.raises(ValueError, match="Expected an iterable of length 2"):
        norm.vmin = (1, 2, 3)
    with pytest.raises(ValueError, match="Expected an iterable of length 2"):
        norm.vmax = (1, 2, 3)

