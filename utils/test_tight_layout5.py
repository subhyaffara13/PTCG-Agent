
def test_tight_layout5():
    """Test tight_layout for image."""
    ax = plt.subplot()
    arr = np.arange(100).reshape((10, 10))
    ax.imshow(arr, interpolation="none")
    plt.tight_layout()

