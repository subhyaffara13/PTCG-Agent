
def test_colorbar_lognorm_extension(extend):
    # Test that colorbar with lognorm is extended correctly
    f, ax = plt.subplots()
    cb = Colorbar(ax, norm=LogNorm(vmin=0.1, vmax=1000.0),
                  orientation='vertical', extend=extend)
    assert cb._values[0] >= 0.0

