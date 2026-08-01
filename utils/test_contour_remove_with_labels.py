
def test_contour_remove_with_labels():
    ax = plt.figure().add_subplot()
    cs = ax.contour(np.arange(16).reshape((4, 4)))
    labels = cs.clabel()
    labels[0].remove()
    with pytest.warns(UserWarning, match="Some labels were manually removed"):
        cs.remove()

