
def test_passing_location(fig_ref, fig_test):
    ax_ref = fig_ref.add_subplot()
    im = ax_ref.imshow([[0, 1], [2, 3]])
    ax_ref.get_figure().colorbar(im, cax=ax_ref.inset_axes([0, 1.05, 1, 0.05]),
                                 orientation="horizontal", ticklocation="top")
    ax_test = fig_test.add_subplot()
    im = ax_test.imshow([[0, 1], [2, 3]])
    ax_test.get_figure().colorbar(im, cax=ax_test.inset_axes([0, 1.05, 1, 0.05]),
                                  location="top")

