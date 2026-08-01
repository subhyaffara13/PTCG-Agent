
def test_find_nearest_contour():
    xy = np.indices((15, 15))
    img = np.exp(-np.pi * (np.sum((xy - 5)**2, 0)/5.**2))
    cs = plt.contour(img, 10)

    nearest_contour = cs.find_nearest_contour(1, 1, pixel=False)
    expected_nearest = (1, 0, 33, 1.965966, 1.965966, 1.866183)
    assert_array_almost_equal(nearest_contour, expected_nearest)

    nearest_contour = cs.find_nearest_contour(8, 1, pixel=False)
    expected_nearest = (1, 0, 5, 7.550173, 1.587542, 0.547550)
    assert_array_almost_equal(nearest_contour, expected_nearest)

    nearest_contour = cs.find_nearest_contour(2, 5, pixel=False)
    expected_nearest = (3, 0, 21, 1.884384, 5.023335, 0.013911)
    assert_array_almost_equal(nearest_contour, expected_nearest)

    nearest_contour = cs.find_nearest_contour(2, 5, indices=(5, 7), pixel=False)
    expected_nearest = (5, 0, 16, 2.628202, 5.0, 0.394638)
    assert_array_almost_equal(nearest_contour, expected_nearest)

