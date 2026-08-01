
def test_colorbar_extension_inverted_axis(orientation, extend, expected):
    """Test extension color with an inverted axis"""
    data = np.arange(12).reshape(3, 4)
    fig, ax = plt.subplots()
    cmap = mpl.colormaps["viridis"].with_extremes(under=(0, 0, 0, 1),
                                                  over=(1, 1, 1, 1))
    im = ax.imshow(data, cmap=cmap)
    cbar = fig.colorbar(im, orientation=orientation, extend=extend)
    if orientation == "horizontal":
        cbar.ax.invert_xaxis()
    else:
        cbar.ax.invert_yaxis()
    assert cbar._extend_patches[0].get_facecolor() == expected
    if extend == "both":
        assert len(cbar._extend_patches) == 2
        assert cbar._extend_patches[1].get_facecolor() == (0, 0, 0, 1)
    else:
        assert len(cbar._extend_patches) == 1

