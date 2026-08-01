
def test_interp_nearest_vs_none():
    """Test the effect of "nearest" and "none" interpolation"""
    # Setting dpi to something really small makes the difference very
    # visible. This works fine with pdf, since the dpi setting doesn't
    # affect anything but images, but the agg output becomes unusably
    # small.
    rcParams['savefig.dpi'] = 3
    X = np.array([[[218, 165, 32], [122, 103, 238]],
                  [[127, 255, 0], [255, 99, 71]]], dtype=np.uint8)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(X, interpolation='none')
    ax1.set_title('interpolation none')
    ax2.imshow(X, interpolation='nearest')
    ax2.set_title('interpolation nearest')

