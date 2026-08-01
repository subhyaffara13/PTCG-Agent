
def istft_compare(Zxx, fs=1.0, window='hann', nperseg=None, noverlap=None,
                  nfft=None, input_onesided=True, boundary=True, time_axis=-1,
                  freq_axis=-2, scaling='spectrum'):
    """Assert that the results from the existing `istft()` and
    `_istft_wrapper()` are close to each other.

    Quirks:
    * If ``boundary=False`` the comparison is skipped, since it does not
      make sense with ShortTimeFFT.istft(). Only used in test
      TestSTFT.test_roundtrip_boundary_extension().
    * If ShortTimeFFT.istft() decides the STFT is not invertible, the
      comparison is skipped, since istft() only emits a warning and does not
      return a correct result. Only used in
      ShortTimeFFT.test_roundtrip_not_nola().
    * For comparing the signals an absolute tolerance of the floating point
      resolution was added to account for the low accuracy of float32 (Occurs
      only in TestSTFT.test_roundtrip_float32()).
    """
    kw = dict(Zxx=Zxx, fs=fs, window=window, nperseg=nperseg,
              noverlap=noverlap, nfft=nfft, input_onesided=input_onesided,
              boundary=boundary, time_axis=time_axis, freq_axis=freq_axis,
              scaling=scaling)

    t, x = istft(**kw)
    if not boundary:  # skip test_roundtrip_boundary_extension():
        return t, x  # _istft_wrapper does() not implement this case
    try:  # if inversion fails, istft() only emits a warning:
        t_wrapper, x_wrapper, (k_lo, k_hi) = _istft_wrapper(**kw)
    except ValueError as v:  # Do nothing if inversion fails:
        if v.args[0] == "Short-time Fourier Transform not invertible!":
            return t, x
        raise v

    e_msg_part = " of `istft_wrapper()` differ from `istft()`"
    assert_allclose(t, t_wrapper, err_msg=f"Sample times {e_msg_part}")

    # Adapted tolerances to account for resolution loss:
    atol = np.finfo(x.dtype).resolution*2  # instead of default atol = 0
    rtol = 1e-7  # default for np.allclose()

    # Relax atol on 32-Bit platforms a bit to pass CI tests.
    #  - Not clear why there are discrepancies (in the FFT maybe?)
    #  - Not sure what changed on 'i686' since earlier on those test passed
    if x.dtype == np.float32 and platform.machine() == 'i686':
        # float32 gets only used by TestSTFT.test_roundtrip_float32() so
        # we are using the tolerances from there to circumvent CI problems
        atol, rtol = 1e-4, 1e-5
    else:
        atol = max(atol, 1e-12)  # 2e-15 seems too tight

    assert_allclose(x_wrapper[k_lo:k_hi], x[k_lo:k_hi], atol=atol, rtol=rtol,
                    err_msg=f"Signal values {e_msg_part}")
    return t, x

