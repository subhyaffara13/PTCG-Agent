
def test_patch_has_dashed_edge():
    """Test _has_dashed_edge method for patches."""
    patch = Rectangle((0, 0), 1, 1)
    patch.set_linestyle('solid')
    assert not patch._has_dashed_edge()

    patch.set_linestyle('--')
    assert patch._has_dashed_edge()

    patch.set_linestyle(':')
    assert patch._has_dashed_edge()

    patch.set_linestyle('-.')
    assert patch._has_dashed_edge()

    # Test custom linestyle
    patch.set_linestyle((0, (2, 2, 10, 2)))
    assert patch._has_dashed_edge()

