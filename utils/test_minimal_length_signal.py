
def test_minimal_length_signal(m_num):
    """Verify that the shortest allowed signal works. """
    SFT = ShortTimeFFT(np.ones(m_num), m_num//2, fs=1)
    n = math.ceil(m_num/2)
    x = np.ones(n)
    Sx = SFT.stft(x)
    x1 = SFT.istft(Sx, k1=n)
    xp_assert_close(x1, x, err_msg=f"Roundtrip minimal length signal ({n=})" +
                                   f" for {m_num} sample window failed!")
    with pytest.raises(ValueError, match=rf"len\(x\)={n-1} must be >= ceil.*"):
        SFT.stft(x[:-1])
    with pytest.raises(ValueError, match=rf"S.shape\[t_axis\]={Sx.shape[1]-1}"
                       f" needs to have at least {Sx.shape[1]} slices"):
        SFT.istft(Sx[:, :-1], k1=n)

