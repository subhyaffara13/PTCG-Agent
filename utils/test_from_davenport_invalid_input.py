
def test_from_davenport_invalid_input(xp):
    ez = [0, 0, 1]
    ey = [0, 1, 0]
    ezy = [0, 1, 1]
    # We can only raise in non-lazy frameworks.
    axes = xp.asarray([ez, ezy])
    if is_lazy_array(axes):
        q = Rotation.from_davenport(axes, 'e', [0, 0]).as_quat()
        assert xp.all(xp.isnan(q))
    else:
        with pytest.raises(ValueError, match="must be orthogonal"):
            Rotation.from_davenport(axes, 'e', [0, 0])
    axes = xp.asarray([ez, ey, ezy])
    if is_lazy_array(axes):
        q = Rotation.from_davenport(axes, 'e', [0, 0, 0]).as_quat()
        assert xp.all(xp.isnan(q))
    else:
        with pytest.raises(ValueError, match="must be orthogonal"):
            Rotation.from_davenport(axes, 'e', [0, 0, 0])
    with pytest.raises(ValueError, match="order should be"):
        Rotation.from_davenport(xp.asarray([ez]), 'xyz', [0])
    with pytest.raises(ValueError, match="Expected `angles`"):
        Rotation.from_davenport(xp.asarray([ez, ey, ez]), 'e', [0, 1, 2, 3])
    with pytest.raises(ValueError, match="Expected `angles`"):  # Too many angles
        Rotation.from_davenport(xp.asarray(ez), 'e', [0, 1])
    with pytest.raises(ValueError, match="Expected `angles`"):  # Too few angles
        Rotation.from_davenport(xp.asarray([ez, ey, ez]), 'e', [0, 1])

