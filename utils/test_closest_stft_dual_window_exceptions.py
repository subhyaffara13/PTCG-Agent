
def test_closest_STFT_dual_window_exceptions():
    """Raise all exceptions in `closest_STFT_dual_window`."""
    with pytest.raises(ValueError, match="Parameters `win` and `desired_dual` are.*"):
        closest_STFT_dual_window(np.ones(4), 2, np.ones(5))
    with pytest.raises(ValueError, match="Parameters `win` and `desired_dual` are.*"):
        closest_STFT_dual_window(np.ones((4, 1)), 2, np.ones(4))
    with pytest.raises(ValueError, match="Parameter win must have finite entries!"):
        closest_STFT_dual_window(np.ones(4)*np.nan, 2, np.ones(4))
    with pytest.raises(ValueError, match="Parameter desired_dual must have finite.*"):
        closest_STFT_dual_window(np.ones(4), 2, np.ones(4)*np.nan)
    with pytest.raises(ValueError, match="Parameter hop=20 is not an integer.*"):
        closest_STFT_dual_window(np.ones(4), 20, np.ones(4))
    with pytest.raises(ValueError, match="Parameter hop=2.0 is not an integer.*"):
        # noinspection PyTypeChecker
        closest_STFT_dual_window(np.ones(4), 2., np.ones(4))

    with pytest.raises(ValueError, match="Unable to calculate scaled closest dual.*"):
        closest_STFT_dual_window(np.ones(4), 2, np.zeros(4), scaled=True)

