
def test_buffer_size(fig_test, fig_ref):
    # On old versions of the Agg renderer, large non-ascii single-character
    # strings (here, "€") would be rendered clipped because the rendering
    # buffer would be set by the physical size of the smaller "a" character.
    ax = fig_test.add_subplot()
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["€", "a"])
    ax.yaxis.majorTicks[1].label1.set_color("w")
    ax = fig_ref.add_subplot()
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["€", ""])

