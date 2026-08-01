
def test_default_device():
    assert info.default_device() == "cpu" == np.asarray(0).device

