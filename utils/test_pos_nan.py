
def test_pos_nan():
    """Check np.nan is a positive nan."""
    assert_(np.signbit(np.nan) == 0)

