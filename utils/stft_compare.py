
def stft_compare(x, fs=1.0, window='hann', nperseg=256, noverlap=None,
                 nfft=None, detrend=False, return_onesided=True,
                 boundary='zeros', padded=True, axis=-1, scaling='spectrum'):
    """Assert that the results from the existing `stft()` and `_stft_wrapper()`
    are close to each other.

    For comparing the STFT values an absolute tolerance of the floating point
    resolution was added to circumvent problems with the following tests:
    * For float32 the tolerances are much higher in
      TestSTFT.test_roundtrip_float32()).
    * The TestSTFT.test_roundtrip_scaling() has a high relative deviation.
      Interestingly this did not appear in Scipy 1.9.1 but only in the current
      development version.
    """
    kw = dict(x=x, fs=fs, window=window, nperseg=nperseg, noverlap=noverlap,
              nfft=nfft, detrend=detrend, return_onesided=return_onesided,
              boundary=boundary, padded=padded, axis=axis, scaling=scaling)
    f, t, Zxx = stft(**kw)
    f_wrapper, t_wrapper, Zxx_wrapper = _stft_wrapper(**kw)

    e_msg_part = " of `stft_wrapper()` differ from `stft()`."
    assert_allclose(f_wrapper, f, err_msg=f"Frequencies {e_msg_part}")
    assert_allclose(t_wrapper, t, err_msg=f"Time slices {e_msg_part}")

    # Adapted tolerances to account for:
    atol = np.finfo(Zxx.dtype).resolution * 2
    assert_allclose(Zxx_wrapper, Zxx, atol=atol,
                    err_msg=f"STFT values {e_msg_part}")
    return f, t, Zxx

