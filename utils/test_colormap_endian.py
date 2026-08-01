
def test_colormap_endian():
    """
    GitHub issue #1005: a bug in putmask caused erroneous
    mapping of 1.0 when input from a non-native-byteorder
    array.
    """
    cmap = mpl.colormaps["jet"]
    # Test under, over, and invalid along with values 0 and 1.
    a = [-0.5, 0, 0.5, 1, 1.5, np.nan]
    for dt in ["f2", "f4", "f8"]:
        anative = np.ma.masked_invalid(np.array(a, dtype=dt))
        aforeign = anative.byteswap().view(anative.dtype.newbyteorder())
        assert_array_equal(cmap(anative), cmap(aforeign))

