
def test_t():
    """Verify that the times of the slices are correct. """
    SFT = ShortTimeFFT(np.ones(8), hop=4, fs=2)
    assert SFT.T == 1/2
    assert SFT.fs == 2.
    assert SFT.delta_t == 4 * 1/2
    t_stft = np.arange(0, SFT.p_max(10)) * SFT.delta_t
    xp_assert_equal(SFT.t(10), t_stft)
    xp_assert_equal(SFT.t(10, 1, 3), t_stft[1:3])
    SFT.T = 1/4
    assert SFT.T == 1/4
    assert SFT.fs == 4
    SFT.fs = 1/8
    assert SFT.fs == 1/8
    assert SFT.T == 8
    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        SFT.t(1.5)  # only integers allowed
    with pytest.raises(ValueError):
        SFT.t(-1)  # only positive `n` allowed

