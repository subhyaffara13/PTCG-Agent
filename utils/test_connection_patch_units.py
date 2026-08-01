
def test_connection_patch_units(pd):
    # tests that this doesn't raise an error
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 5))
    x = pd.Timestamp('2017-01-01T12')
    ax1.axvline(x)
    y = "test test"
    ax2.axhline(y)
    arr = mpatches.ConnectionPatch((x, 0), (0, y),
                                   coordsA='data', coordsB='data',
                                   axesA=ax1, axesB=ax2)
    fig.add_artist(arr)
    fig.draw_without_rendering()

