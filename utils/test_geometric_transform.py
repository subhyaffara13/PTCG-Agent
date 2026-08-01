
def test_geometric_transform():
    def transform(output_coordinates, shift):
        return output_coordinates[0] - shift, output_coordinates[1] - shift

    def check(j):
        func = TRANSFORM_FUNCTIONS[j]

        im = np.arange(12).reshape(4, 3).astype(np.float64)
        shift = 0.5

        res = ndimage.geometric_transform(im, func(shift))
        std = ndimage.geometric_transform(im, transform, extra_arguments=(shift,))
        xp_assert_close(res, std, err_msg=f"#{j} failed")

    for j, func in enumerate(TRANSFORM_FUNCTIONS):
        check(j)

