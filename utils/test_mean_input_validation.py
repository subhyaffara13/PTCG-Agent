
def test_mean_input_validation(xp):
    r = Rotation.from_quat(xp.eye(4))
    if is_lazy_array(r.as_quat()):
        m = r.mean(weights=-xp.ones(4))
        assert xp.all(xp.isnan(m._quat))
    else:
        with pytest.raises(ValueError, match="non-negative"):
            r.mean(weights=-xp.ones(4))

    # Test weight shape mismatch
    r = Rotation.from_quat(xp.ones((3, 4)))
    with pytest.raises(ValueError, match="Expected `weights` to"):
        r.mean(weights=xp.ones((2,)))
    r = Rotation.from_quat(xp.ones((2, 3, 4)))
    with pytest.raises(ValueError, match="Expected `weights` to"):
        r.mean(weights=xp.ones((2, 2)))

    # Test wrong axis
    with pytest.raises(ValueError, match=r"axis .* is out of bounds"):
        r.mean(axis=3)
    with pytest.raises(ValueError, match=r"axis .* is out of bounds"):
        r.mean(axis=(-1, 2))
    with pytest.raises(ValueError, match="`axis` must be None, int, or tuple of ints."):
        r.mean(axis="0")
    with pytest.raises(ValueError, match=r"axis .* is out of bounds"):
        r.mean(axis=-12)

