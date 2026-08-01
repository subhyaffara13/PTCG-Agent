
def test_contour_remove():
    ax = plt.figure().add_subplot()
    orig_children = ax.get_children()
    cs = ax.contour(np.arange(16).reshape((4, 4)))
    cs.clabel()
    assert ax.get_children() != orig_children
    cs.remove()
    assert ax.get_children() == orig_children

