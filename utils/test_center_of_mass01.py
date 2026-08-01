
def test_center_of_mass01(xp):
    expected = (0.0, 0.0)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[1, 0], [0, 0]], dtype=dtype)
        output = ndimage.center_of_mass(input)
        assert output == expected

