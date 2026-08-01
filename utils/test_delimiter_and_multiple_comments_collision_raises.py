
def test_delimiter_and_multiple_comments_collision_raises():
    with pytest.raises(
        TypeError, match="Comment characters.*cannot include the delimiter"
    ):
        np.loadtxt(StringIO("1, 2, 3"), delimiter=",", comments=["#", ","])

