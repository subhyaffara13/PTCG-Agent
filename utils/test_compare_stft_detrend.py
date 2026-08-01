
def test_compare_stft_detrend():
    """Test the detrending in `ShortTimeFFT.stft_detrend()`. """
    SFT = ShortTimeFFT(np.ones(4), 4, fs=1)
    x0 = np.zeros(4) # signal without trend
    x1 = x0 + 3  # signal with constant trend
    x2 = x0 + np.arange(len(x0))  # signal with linear trend

    kw = dict(k_offset=2, p1=1)  # we want only one slice
    Sx0 = SFT.stft(x0, **kw)  # no trend
    Sx1 = SFT.stft_detrend(x1, detr='constant', **kw)
    Sx2 = SFT.stft_detrend(x2, detr='linear', **kw)
    Sx3 = SFT.stft_detrend(x1, detr=lambda x: x - np.mean(x), **kw)

    atol = np.finfo(Sx0.dtype).resolution * 5  # needed to compare with array of zeros
    xp_assert_close(Sx1, Sx0, atol=atol, err_msg="Constant detrending failed!")
    xp_assert_close(Sx0, Sx2, atol=atol, err_msg="Linear detrending failed!")
    xp_assert_close(Sx0, Sx3, atol=atol, err_msg="Detrending using a function failed!")

