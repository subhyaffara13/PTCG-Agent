
def test_image_composite_alpha():
    """
    Tests that the alpha value is recognized and correctly applied in the
    process of compositing images together.
    """
    fig, ax = plt.subplots()
    arr = np.zeros((11, 21, 4))
    arr[:, :, 0] = 1
    arr[:, :, 3] = np.concatenate(
        (np.arange(0, 1.1, 0.1), np.arange(0, 1, 0.1)[::-1]))
    arr2 = np.zeros((21, 11, 4))
    arr2[:, :, 0] = 1
    arr2[:, :, 1] = 1
    arr2[:, :, 3] = np.concatenate(
        (np.arange(0, 1.1, 0.1), np.arange(0, 1, 0.1)[::-1]))[:, np.newaxis]
    ax.imshow(arr, extent=[1, 2, 5, 0], alpha=0.3)
    ax.imshow(arr, extent=[2, 3, 5, 0], alpha=0.6)
    ax.imshow(arr, extent=[3, 4, 5, 0])
    ax.imshow(arr2, extent=[0, 5, 1, 2])
    ax.imshow(arr2, extent=[0, 5, 2, 3], alpha=0.6)
    ax.imshow(arr2, extent=[0, 5, 3, 4], alpha=0.3)
    ax.set_facecolor((0, 0.5, 0, 1))
    ax.set_xlim(0, 5)
    ax.set_ylim(5, 0)

