
def test_connection_patch_pixel_points(fig_test, fig_ref):
    xyA_pts = (.3, .2)
    xyB_pts = (-30, -20)

    ax1, ax2 = fig_test.subplots(1, 2)
    con = mpatches.ConnectionPatch(xyA=xyA_pts, coordsA="axes points", axesA=ax1,
                                   xyB=xyB_pts, coordsB="figure points",
                                   arrowstyle="->", shrinkB=5)
    fig_test.add_artist(con)

    plt.rcParams["savefig.dpi"] = plt.rcParams["figure.dpi"]

    ax1, ax2 = fig_ref.subplots(1, 2)
    xyA_pix = (xyA_pts[0]*(fig_ref.dpi/72), xyA_pts[1]*(fig_ref.dpi/72))
    xyB_pix = (xyB_pts[0]*(fig_ref.dpi/72), xyB_pts[1]*(fig_ref.dpi/72))
    con = mpatches.ConnectionPatch(xyA=xyA_pix, coordsA="axes pixels", axesA=ax1,
                                   xyB=xyB_pix, coordsB="figure pixels",
                                   arrowstyle="->", shrinkB=5)
    fig_ref.add_artist(con)

