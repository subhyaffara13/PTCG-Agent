
def test_colorbar_closed_patch():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_axes((0.05, 0.85, 0.9, 0.1))
    ax2 = fig.add_axes((0.1, 0.65, 0.75, 0.1))
    ax3 = fig.add_axes((0.05, 0.45, 0.9, 0.1))
    ax4 = fig.add_axes((0.05, 0.25, 0.9, 0.1))
    ax5 = fig.add_axes((0.05, 0.05, 0.9, 0.1))

    cmap = mpl.colormaps["RdBu"].resampled(5)

    im = ax1.pcolormesh(np.linspace(0, 10, 16).reshape((4, 4)), cmap=cmap)

    # The use of a "values" kwarg here is unusual.  It works only
    # because it is matched to the data range in the image and to
    # the number of colors in the LUT.
    values = np.linspace(0, 10, 5)
    cbar_kw = dict(orientation='horizontal', values=values, ticks=[])

    # The wide line is to show that the closed path is being handled
    # correctly.  See PR #4186.
    with rc_context({'axes.linewidth': 16}):
        plt.colorbar(im, cax=ax2, extend='both', extendfrac=0.5, **cbar_kw)
        plt.colorbar(im, cax=ax3, extend='both', **cbar_kw)
        plt.colorbar(im, cax=ax4, extend='both', extendrect=True, **cbar_kw)
        plt.colorbar(im, cax=ax5, extend='neither', **cbar_kw)

