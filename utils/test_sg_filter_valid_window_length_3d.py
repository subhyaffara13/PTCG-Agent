
def test_sg_filter_valid_window_length_3d(xp):
    """Tests that the window_length check is using the correct axis."""

    x = xp.ones((10, 20, 30))

    savgol_filter(x, window_length=29, polyorder=3, mode='interp')

    with pytest.raises(ValueError, match='window_length must be less than'):
        # window_length is more than x.shape[-1].
        savgol_filter(x, window_length=31, polyorder=3, mode='interp')

    savgol_filter(x, window_length=9, polyorder=3, axis=0, mode='interp')

    with pytest.raises(ValueError, match='window_length must be less than'):
        # window_length is more than x.shape[0].
        savgol_filter(x, window_length=11, polyorder=3, axis=0, mode='interp')

