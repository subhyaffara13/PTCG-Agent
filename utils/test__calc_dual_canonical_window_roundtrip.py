
def test__calc_dual_canonical_window_roundtrip():
    """Test dual window calculation with a round trip to verify duality.

    Note that this works only for canonical window pairs (having minimal
    energy) like a Gaussian.

    The window is the same as in the example of `from ShortTimeFFT.from_dual`.
    """
    win = gaussian(51, std=10, sym=True)
    d_win = _calc_dual_canonical_window(win, 10)
    win2 = _calc_dual_canonical_window(d_win, 10)
    xp_assert_close(win2, win)

