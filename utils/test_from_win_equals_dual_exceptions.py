
def test_from_win_equals_dual_exceptions():
    """Raise all occurring exceptions in `ShortTimeFFT.from_closest_win_equals_dual`.
    """
    with pytest.raises(ValueError, match="Parameter desired_win is not 1d, but.*"):
        ShortTimeFFT.from_win_equals_dual(np.ones((3, 4)), hop=1, fs=1)
    with pytest.raises(ValueError, match="Parameter desired_win cannot be of int.*"):
        ShortTimeFFT.from_win_equals_dual(np.ones(4, dtype=int), hop=1, fs=1)
    with pytest.raises(ValueError, match="Parameter desired_win is not 1d, but.*"):
        ShortTimeFFT.from_win_equals_dual(np.array([]), hop=1, fs=1)
    with pytest.raises(ValueError, match="Parameter desired_win must have finite.*"):
        ShortTimeFFT.from_win_equals_dual(np.ones(3) * np.inf, hop=1, fs=1)
    with pytest.raises(ValueError, match="Parameter hop=0 is not an integer .*"):
        ShortTimeFFT.from_win_equals_dual(np.ones(4), hop=0, fs=1)
    with pytest.raises(ValueError, match="Parameter hop=5 is not an integer .*"):
        ShortTimeFFT.from_win_equals_dual(np.ones(4), hop=5, fs=1)

    with pytest.raises(ValueError, match="P.+ desired_win does not have valid.*"):
        w = np.array([1, 0, 1, 0, 1], dtype=float)
        ShortTimeFFT.from_win_equals_dual(w, hop=2, fs=1)
    with pytest.raises(ValueError, match="Parameter scale_to='invalid' not in.*"):
        # noinspection PyTypeChecker
        ShortTimeFFT.from_win_equals_dual(w, hop=2, fs=1, scale_to='invalid')

