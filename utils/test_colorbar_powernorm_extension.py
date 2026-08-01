
def test_colorbar_powernorm_extension():
    # Test that colorbar with powernorm is extended correctly
    # Just a smoke test that adding the colorbar doesn't raise an error or warning
    fig, ax = plt.subplots()
    Colorbar(ax, norm=PowerNorm(gamma=0.5, vmin=0.0, vmax=1.0),
             orientation='vertical', extend='both')

