
def test_center_of_mass09(xp):
    labels = xp.asarray((1, 2))
    expected = xp.asarray([(0.5, 0.0), (0.5, 1.0)], dtype=xp.float64)
    input = np.asarray([[1, 2], [1, 1]], dtype=bool)
    input = xp.asarray(input)
    output = ndimage.center_of_mass(input, labels, xp.asarray([1, 2]))
    xp_assert_equal(xp.asarray(output), xp.asarray(expected))

