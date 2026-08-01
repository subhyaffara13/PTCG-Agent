
def test_from_win_equals_dual_unitary():
    """Check that STFT can be unitary mapping. """
    m, hop = 8, 4
    des_win = get_window('hann', m)
    SFT = ShortTimeFFT.from_win_equals_dual(des_win, hop, 1, fft_mode='twosided',
                                            scale_to='unitary')
    # Orthogonal signals:
    x, y = np.tile([-1, -1, 1, 1], 4), np.tile([1, -1, -1, 1], 4)
    Sxx, Sxy = SFT.spectrogram(x), SFT.spectrogram(x, y)

    atol = np.finfo(Sxx.dtype).resolution
    assert sum(x * y) == 0
    xp_assert_close(np.sum(Sxx), np.sum(x ** 2, dtype=Sxx.dtype), atol=atol,
                    err_msg="Energies do not match!")
    xp_assert_close(np.sum(Sxy), 0.0j, atol=atol,
                    err_msg="STFT scalar product of Sx and Sy not 0!")
    xp_assert_close(SFT.dual_win, SFT.win*SFT.m_num, atol=atol,
                    err_msg="Wrong factor for dual_win/win!")

