
def test_wheel_info(filename, info):
    if inspect.isclass(info):
        with pytest.raises(info):
            Wheel(filename)
        return
    w = Wheel(filename)
    assert {k: getattr(w, k) for k in info.keys()} == info

