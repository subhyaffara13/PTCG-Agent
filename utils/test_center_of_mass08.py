
def test_center_of_mass08(xp):
    labels = xp.asarray([1, 2])
    expected = (0.5, 1.0)
    input = np.asarray([[5, 2], [3, 1]], dtype=bool)
    input = xp.asarray(input)
    output = ndimage.center_of_mass(input, labels, 2)
    assert output == expected

