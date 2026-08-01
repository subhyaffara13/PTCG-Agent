
def test_freq_window_not_implemented(window):
    # GH 15354
    df = DataFrame(
        np.arange(10),
        index=date_range("2015-12-24", periods=10, freq="D"),
    )
    with pytest.raises(
        NotImplementedError, match="^step (not implemented|is not supported)"
    ):
        df.rolling(window, step=3).sum()

