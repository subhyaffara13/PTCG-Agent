
def test_delimiter_comment_collision_raises():
    with pytest.raises(TypeError, match=".*control characters.*incompatible"):
        np.loadtxt(StringIO("1, 2, 3"), delimiter=",", comments=",")

