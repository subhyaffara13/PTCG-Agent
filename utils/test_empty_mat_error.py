
def test_empty_mat_error():
    # Test we get a specific warning for an empty mat file
    sio = BytesIO()
    assert_raises(MatReadError, loadmat, sio)

