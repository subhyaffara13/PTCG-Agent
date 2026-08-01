
def test_imshow_norm_vminvmax():
    """Parameters vmin, vmax should error if norm is given."""
    a = [[1, 2], [3, 4]]
    ax = plt.axes()
    with pytest.raises(ValueError,
                       match="Passing a Normalize instance simultaneously "
                             "with vmin/vmax is not supported."):
        ax.imshow(a, norm=mcolors.Normalize(-10, 10), vmin=0, vmax=5)

