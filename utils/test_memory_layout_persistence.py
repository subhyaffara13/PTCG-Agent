
def test_memory_layout_persistence(mode):
    """Test if C and F order is preserved for all pad modes."""
    x = np.ones((5, 10), order='C')
    assert np.pad(x, 5, mode).flags["C_CONTIGUOUS"]
    x = np.ones((5, 10), order='F')
    assert np.pad(x, 5, mode).flags["F_CONTIGUOUS"]

