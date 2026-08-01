
def test_kwargs(mode):
    """Test behavior of pad's kwargs for the given mode."""
    allowed = _all_modes[mode]
    not_allowed = {}
    for kwargs in _all_modes.values():
        if kwargs != allowed:
            not_allowed.update(kwargs)
    # Test if allowed keyword arguments pass
    np.pad([1, 2, 3], 1, mode, **allowed)
    # Test if prohibited keyword arguments of other modes raise an error
    for key, value in not_allowed.items():
        match = f"unsupported keyword arguments for mode '{mode}'"
        with pytest.raises(ValueError, match=match):
            np.pad([1, 2, 3], 1, mode, **{key: value})


def test_kwargs():
    fig, ax = plt.subplots(constrained_layout={'h_pad': 0.02})
    fig.draw_without_rendering()

