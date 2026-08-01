
def test_scaledrotation_get_matrix_invalid():
    """Test get_matrix when the matrix is invalid and needs recalculation."""
    theta = np.pi / 2
    trans_shift = MagicMock(transform=MagicMock(return_value=[[theta, 0]]))
    scaled_rot = _ScaledRotation(theta, trans_shift)
    scaled_rot._invalid = True
    matrix = scaled_rot.get_matrix()
    trans_shift.transform.assert_called_once_with([[theta, 0]])
    expected_rotation = np.array([[0, -1],
                                  [1,  0]])
    assert matrix is not None
    assert_allclose(matrix[:2, :2], expected_rotation, atol=1e-15)

