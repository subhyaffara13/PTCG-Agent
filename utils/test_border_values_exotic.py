
def test_border_values_exotic():
    """Ensure that the border calculations are correct for windows with
    zeros. """
    w = np.array([0, 0, 0, 0, 0, 0, 0, 1.])
    SFT = ShortTimeFFT(w, hop=1, fs=1)
    assert SFT.lower_border_end == (0, 0)

    SFT = ShortTimeFFT(np.flip(w), hop=20, fs=1)
    assert SFT.upper_border_begin(4) == (16, 1)
    assert SFT.upper_border_begin(5) == (16, 1)
    assert SFT.upper_border_begin(23) == (36, 2)
    assert SFT.upper_border_begin(24) == (36, 2)
    assert SFT.upper_border_begin(25) == (36, 2)

    SFT._hop = -1  # provoke unreachable line
    with pytest.raises(RuntimeError):
        _ = SFT.k_max(4)
    with pytest.raises(RuntimeError):
        _ = SFT.k_min

