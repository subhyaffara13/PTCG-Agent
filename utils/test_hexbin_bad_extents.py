
def test_hexbin_bad_extents():
    fig, ax = plt.subplots()
    data = (np.arange(20) / 20).reshape((2, 10))
    x, y = data

    with pytest.raises(ValueError, match="In extent, xmax must be greater than xmin"):
        ax.hexbin(x, y, extent=(1, 0, 0, 1))

    with pytest.raises(ValueError, match="In extent, ymax must be greater than ymin"):
        ax.hexbin(x, y, extent=(0, 1, 1, 0))

