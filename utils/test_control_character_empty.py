
def test_control_character_empty():
    with pytest.raises(TypeError, match="Text reading control character must"):
        np.loadtxt(StringIO("1 2 3"), delimiter="")
    with pytest.raises(TypeError, match="Text reading control character must"):
        np.loadtxt(StringIO("1 2 3"), quotechar="")
    with pytest.raises(ValueError, match="comments cannot be an empty string"):
        np.loadtxt(StringIO("1 2 3"), comments="")
    with pytest.raises(ValueError, match="comments cannot be an empty string"):
        np.loadtxt(StringIO("1 2 3"), comments=["#", ""])

