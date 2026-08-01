
def test_set_alpha():
    art = martist.Artist()
    with pytest.raises(TypeError, match='^alpha must be numeric or None'):
        art.set_alpha('string')
    with pytest.raises(TypeError, match='^alpha must be numeric or None'):
        art.set_alpha([1, 2, 3])
    with pytest.raises(ValueError, match="outside 0-1 range"):
        art.set_alpha(1.1)
    with pytest.raises(ValueError, match="outside 0-1 range"):
        art.set_alpha(np.nan)

