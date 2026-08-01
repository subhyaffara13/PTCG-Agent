
def test_center_of_mass02(xp):
    expected = (1, 0)
    for type in types:
        dtype = getattr(xp, type)
        input = xp.asarray([[0, 0], [1, 0]], dtype=dtype)
        output = ndimage.center_of_mass(input)
        assert output == expected

