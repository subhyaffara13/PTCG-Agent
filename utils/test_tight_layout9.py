
def test_tight_layout9():
    # Test tight_layout for non-visible subplots
    # GH 8244
    f, axarr = plt.subplots(2, 2)
    axarr[1][1].set_visible(False)
    plt.tight_layout()

