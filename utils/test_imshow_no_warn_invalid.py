
def test_imshow_no_warn_invalid():
    plt.imshow([[1, 2], [3, np.nan]])  # Check that no warning is emitted.

