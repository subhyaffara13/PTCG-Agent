
def test_generic_filter():
    def filter2d(footprint_elements, weights):
        return (weights*footprint_elements).sum()

    def check(j):
        func = FILTER2D_FUNCTIONS[j]

        im = np.ones((20, 20))
        im[:10,:10] = 0
        footprint = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        footprint_size = np.count_nonzero(footprint)
        weights = np.ones(footprint_size)/footprint_size

        res = ndimage.generic_filter(im, func(weights),
                                     footprint=footprint)
        std = ndimage.generic_filter(im, filter2d, footprint=footprint,
                                     extra_arguments=(weights,))
        xp_assert_close(res, std, err_msg=f"#{j} failed")

    for j, func in enumerate(FILTER2D_FUNCTIONS):
        check(j)

