
def test_center_of_mass07(xp):
    labels = xp.asarray([1, 0])
    expected = (0.5, 0.0)
    input = np.asarray([[1, 2], [3, 1]], dtype=bool)
    input = xp.asarray(input)
    output = ndimage.center_of_mass(input, labels)
    assert output == expected

