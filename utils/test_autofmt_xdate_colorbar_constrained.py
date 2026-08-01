
def test_autofmt_xdate_colorbar_constrained():
    # check works with a colorbar.
    # with constrained layout, colorbars do not have a gridspec,
    # but autofmt_xdate checks if all axes have a gridspec before being
    # applied.
    fig, ax = plt.subplots(layout="constrained")
    im = ax.imshow([[1, 4, 6], [2, 3, 5]])
    plt.colorbar(im)
    fig.autofmt_xdate()
    fig.draw_without_rendering()
    label = ax.get_xticklabels(which='major')[1]
    assert label.get_rotation() == 30.0

