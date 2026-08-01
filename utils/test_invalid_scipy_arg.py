
def test_invalid_scipy_arg():
    # This error is raised by scipy
    pytest.importorskip("scipy")
    msg = r"boxcar\(\) got an unexpected"
    with pytest.raises(TypeError, match=msg):
        Series(range(3)).rolling(1, win_type="boxcar").mean(foo="bar")

