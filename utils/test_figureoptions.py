
def test_figureoptions():
    fig, ax = plt.subplots()
    ax.plot([1, 2])
    ax.imshow([[1]])
    ax.scatter(range(3), range(3), c=range(3))
    with mock.patch("matplotlib.backends.qt_compat._exec", lambda obj: None):
        fig.canvas.manager.toolbar.edit_parameters()

