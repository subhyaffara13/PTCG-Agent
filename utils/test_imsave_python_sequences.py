
def test_imsave_python_sequences():
    # Tests saving an image with data passed using Python sequence types
    # such as lists or tuples.

    # RGB image: 3 rows × 2 columns, with float values in [0.0, 1.0]
    img_data = [
        [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0)],
        [(0.0, 0.0, 1.0), (1.0, 1.0, 0.0)],
        [(0.0, 1.0, 1.0), (1.0, 0.0, 1.0)],
    ]

    buff = io.BytesIO()
    plt.imsave(buff, img_data, format="png")
    buff.seek(0)
    read_img = plt.imread(buff)

    assert_array_equal(
        np.array(img_data),
        read_img[:, :, :3]  # Drop alpha if present
    )

