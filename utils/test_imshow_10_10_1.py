
def test_imshow_10_10_1(fig_test, fig_ref):
    # 10x10x1 should be the same as 10x10
    arr = np.arange(100).reshape((10, 10, 1))
    ax = fig_ref.subplots()
    ax.imshow(arr[:, :, 0], interpolation="bilinear", extent=(1, 2, 1, 2))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

    ax = fig_test.subplots()
    ax.imshow(arr, interpolation="bilinear", extent=(1, 2, 1, 2))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

