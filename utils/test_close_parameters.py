
def test_close_parameters():
    it = np.nditer(np.arange(3))
    assert_raises(TypeError, it.close, 1)

