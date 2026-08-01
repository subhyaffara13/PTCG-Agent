
def test_shadow(fig_test, fig_ref):
    xy = np.array([.2, .3])
    dxy = np.array([.1, .2])
    # We need to work around the nonsensical (dpi-dependent) interpretation of
    # offsets by the Shadow class...
    plt.rcParams["savefig.dpi"] = "figure"
    # Test image.
    a1 = fig_test.subplots()
    rect = mpatches.Rectangle(xy=xy, width=.5, height=.5)
    shadow = mpatches.Shadow(rect, ox=dxy[0], oy=dxy[1])
    a1.add_patch(rect)
    a1.add_patch(shadow)
    # Reference image.
    a2 = fig_ref.subplots()
    rect = mpatches.Rectangle(xy=xy, width=.5, height=.5)
    shadow = mpatches.Rectangle(
        xy=xy + fig_ref.dpi / 72 * dxy, width=.5, height=.5,
        fc=np.asarray(mcolors.to_rgb(rect.get_facecolor())) * .3,
        ec=np.asarray(mcolors.to_rgb(rect.get_facecolor())) * .3,
        alpha=.5)
    a2.add_patch(shadow)
    a2.add_patch(rect)

