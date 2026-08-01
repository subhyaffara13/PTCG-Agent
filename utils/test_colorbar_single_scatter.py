
def test_colorbar_single_scatter():
    # Issue #2642: if a path collection has only one entry,
    # the norm scaling within the colorbar must ensure a
    # finite range, otherwise a zero denominator will occur in _locate.
    plt.figure()
    x = y = [0]
    z = [50]
    cmap = mpl.colormaps['jet'].resampled(16)
    cs = plt.scatter(x, y, z, c=z, cmap=cmap)
    plt.colorbar(cs)

