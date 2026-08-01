
def test_prevent_rasterization(fig_test, fig_ref):
    loc = [0.05, 0.05]

    ax_ref = fig_ref.subplots()

    ax_ref.plot([loc[0]], [loc[1]], marker="x", c="black", zorder=2)

    b = mpl.offsetbox.TextArea("X")
    abox = mpl.offsetbox.AnnotationBbox(b, loc, zorder=2.1)
    ax_ref.add_artist(abox)

    ax_test = fig_test.subplots()
    ax_test.plot([loc[0]], [loc[1]], marker="x", c="black", zorder=2,
                 rasterized=True)

    b = mpl.offsetbox.TextArea("X")
    abox = mpl.offsetbox.AnnotationBbox(b, loc, zorder=2.1)
    ax_test.add_artist(abox)

