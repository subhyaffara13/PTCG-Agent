
def test_mask_image():
    # Test mask image two ways: Using nans and using a masked array.

    fig, (ax1, ax2) = plt.subplots(1, 2)

    A = np.ones((5, 5))
    A[1:2, 1:2] = np.nan

    ax1.imshow(A, interpolation='nearest')

    A = np.zeros((5, 5), dtype=bool)
    A[1:2, 1:2] = True
    A = np.ma.masked_array(np.ones((5, 5), dtype=np.uint16), A)

    ax2.imshow(A, interpolation='nearest')

