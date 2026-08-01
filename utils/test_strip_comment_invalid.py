
def test_strip_comment_invalid():
    with pytest.raises(ValueError, match="Missing closing quote"):
        cbook._strip_comment('grid.color: "aa')

