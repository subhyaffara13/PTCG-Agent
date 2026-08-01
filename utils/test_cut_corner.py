
def test_cut_corner(x, bins, msg):
    with pytest.raises(ValueError, match=msg):
        cut(x, bins)

