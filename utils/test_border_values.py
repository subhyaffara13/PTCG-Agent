
def test_border_values():
    """Ensure that minimum and maximum values of slices are correct."""
    SFT = ShortTimeFFT(np.ones(8), hop=4, fs=1)
    assert SFT.p_min == 0
    assert SFT.k_min == -4
    assert SFT.lower_border_end == (4, 1)
    assert SFT.lower_border_end == (4, 1)  # needed to test caching
    assert SFT.p_max(10) == 4
    assert SFT.k_max(10) == 16
    assert SFT.upper_border_begin(10) == (4, 2)
    assert SFT.upper_border_begin(10) == (4, 2)  # needed to test caching
    # Raise exceptions:
    with pytest.raises(ValueError, match="^Parameter n must be"):
        SFT.upper_border_begin(3)
    with pytest.raises(ValueError, match="^Parameter n must be"):
        SFT._post_padding(3)
    with pytest.raises(RuntimeError):
        SFT._hop = -1  # illegal hop interval
        SFT.upper_border_begin(8)

