
def test_scaledrotation_initialization():
    """Test that the ScaledRotation object is initialized correctly."""
    theta = 1.0  # Arbitrary theta value for testing
    trans_shift = MagicMock()  # Mock the trans_shift transformation
    scaled_rot = _ScaledRotation(theta, trans_shift)
    assert scaled_rot._theta == theta
    assert scaled_rot._trans_shift == trans_shift
    assert scaled_rot._mtx is None

