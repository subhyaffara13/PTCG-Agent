
def test_subplottool():
    fig, ax = plt.subplots()
    with mock.patch("matplotlib.backends.qt_compat._exec", lambda obj: None):
        tool = fig.canvas.manager.toolbar.configure_subplots()
        assert tool is not None
        assert tool == fig.canvas.manager.toolbar.configure_subplots()

