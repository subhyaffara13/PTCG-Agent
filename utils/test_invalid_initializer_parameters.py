
def test_invalid_initializer_parameters():
    """Verify that exceptions get raised on invalid parameters when
    instantiating ShortTimeFFT. """
    with pytest.raises(ValueError, match=r"Parameter win must be 1d, " +
                                         r"but win.shape=\(2, 2\)!"):
        ShortTimeFFT(np.ones((2, 2)), hop=4, fs=1)
    with pytest.raises(ValueError, match="Parameter win must have " +
                                         "finite entries"):
        ShortTimeFFT(np.array([1, np.inf, 2, 3]), hop=4, fs=1)
    with pytest.raises(ValueError, match="Parameter hop=0 is not " +
                                         "an integer >= 1!"):
        ShortTimeFFT(np.ones(4), hop=0, fs=1)
    with pytest.raises(ValueError, match="Parameter hop=2.0 is not " +
                                         "an integer >= 1!"):
        # noinspection PyTypeChecker
        ShortTimeFFT(np.ones(4), hop=2.0, fs=1)
    with pytest.raises(ValueError, match=r"dual_win.shape=\(5,\) must equal " +
                                         r"win.shape=\(4,\)!"):
        ShortTimeFFT(np.ones(4), hop=2, fs=1, dual_win=np.ones(5))
    with pytest.raises(ValueError, match="Parameter dual_win must be " +
                                         "a finite array!"):
        ShortTimeFFT(np.ones(3), hop=2, fs=1,
                     dual_win=np.array([np.nan, 2, 3]))

