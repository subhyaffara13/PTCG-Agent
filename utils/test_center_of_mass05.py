
def test_center_of_mass05(xp):
    expected = (0.5, 0.5)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 1], [1, 1]], dtype=dtype)
        output = ndimage.center_of_mass(input)
        assert output == expected

