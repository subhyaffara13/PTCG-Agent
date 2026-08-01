
def test_center_of_mass03(xp):
    expected = (0, 1)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[0, 1], [0, 0]], dtype=dtype)
        output = ndimage.center_of_mass(input)
        assert output == expected

