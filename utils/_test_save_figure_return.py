
def _test_save_figure_return():
    fig, ax = plt.subplots()
    ax.imshow([[1]])
    prop = "matplotlib.backends._macosx.choose_save_file"
    with mock.patch(prop, return_value="foobar.png"):
        fname = fig.canvas.manager.toolbar.save_figure()
        os.remove("foobar.png")
        assert fname == "foobar.png"
    with mock.patch(prop, return_value=None):
        fname = fig.canvas.manager.toolbar.save_figure()
        assert fname is None

