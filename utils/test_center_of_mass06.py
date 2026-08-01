
def test_center_of_mass06(xp):
    expected = (0.5, 0.5)
    input = np.asarray([[1, 2], [3, 1]], dtype=bool)
    input = xp.asarray(input)
    output = ndimage.center_of_mass(input)
    assert output == expected

