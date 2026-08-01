
def test_val_in_range_base_fallback():
    # Directly test the ScaleBase fallback for custom scales.
    # ScaleBase.limit_range_for_scale returns values unchanged by default
    s = mscale.ScaleBase(axis=None)

    # Normal values should be True
    assert s.val_in_range(1.0) is True
    assert s.val_in_range(-5.5) is True

    # NaN and Inf returns False since they cannot be drawn in a plot
    assert s.val_in_range(np.nan) is False
    assert s.val_in_range(np.inf) is False
    assert s.val_in_range(-np.inf) is False

