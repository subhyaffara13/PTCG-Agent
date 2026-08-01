
def test_cossin_error_empty_subblocks():
    with pytest.raises(ValueError, match="x11.*empty"):
        cossin(([], [], [], []))
    with pytest.raises(ValueError, match="x12.*empty"):
        cossin(([1, 2], [], [6, 7], [8, 9, 10]))
    with pytest.raises(ValueError, match="x21.*empty"):
        cossin(([1, 2], [3, 4, 5], [], [8, 9, 10]))
    with pytest.raises(ValueError, match="x22.*empty"):
        cossin(([1, 2], [3, 4, 5], [2], []))

