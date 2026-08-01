
def test_find_nearest_contour_no_filled():
    xy = np.indices((15, 15))
    img = np.exp(-np.pi * (np.sum((xy - 5)**2, 0)/5.**2))
    cs = plt.contourf(img, 10)

    with pytest.raises(ValueError, match="Method does not support filled contours"):
        cs.find_nearest_contour(1, 1, pixel=False)

    with pytest.raises(ValueError, match="Method does not support filled contours"):
        cs.find_nearest_contour(1, 10, indices=(5, 7), pixel=False)

    with pytest.raises(ValueError, match="Method does not support filled contours"):
        cs.find_nearest_contour(2, 5, indices=(2, 7), pixel=True)

