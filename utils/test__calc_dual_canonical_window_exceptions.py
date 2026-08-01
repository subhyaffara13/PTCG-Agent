
def test__calc_dual_canonical_window_exceptions():
    """Raise all exceptions in `_calc_dual_canonical_window`."""
    # Verify that calculation can fail:
    with pytest.raises(ValueError, match="hop=5 is larger than window len.*"):
        _calc_dual_canonical_window(np.ones(4), 5)
    with pytest.raises(ValueError, match=".* Transform not invertible!"):
        _calc_dual_canonical_window(np.array([.1, .2, .3, 0]), 4)

    # Verify that parameter `win` may not be integers:
    with pytest.raises(ValueError, match="Parameter 'win' cannot be of int.*"):
        _calc_dual_canonical_window(np.ones(4, dtype=int), 1)

