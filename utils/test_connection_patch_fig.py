
def test_connection_patch_fig(fig_test, fig_ref):
    # Test that connection patch can be added as figure artist, and that figure
    # pixels count negative values from the top right corner (this API may be
    # changed in the future).
    ax1, ax2 = fig_test.subplots(1, 2)
    con = mpatches.ConnectionPatch(
        xyA=(.3, .2), coordsA="data", axesA=ax1,
        xyB=(-30, -20), coordsB="figure pixels",
        arrowstyle="->", shrinkB=5)
    fig_test.add_artist(con)

    ax1, ax2 = fig_ref.subplots(1, 2)
    bb = fig_ref.bbox
    # Necessary so that pixel counts match on both sides.
    plt.rcParams["savefig.dpi"] = plt.rcParams["figure.dpi"]
    con = mpatches.ConnectionPatch(
        xyA=(.3, .2), coordsA="data", axesA=ax1,
        xyB=(bb.width - 30, bb.height - 20), coordsB="figure pixels",
        arrowstyle="->", shrinkB=5)
    fig_ref.add_artist(con)

