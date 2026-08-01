
def test_toolbar_zoompan():
    with pytest.warns(UserWarning, match=_EXPECTED_WARNING_TOOLMANAGER):
        plt.rcParams['toolbar'] = 'toolmanager'
    ax = plt.gca()
    fig = ax.get_figure()
    assert ax.get_navigate_mode() is None
    fig.canvas.manager.toolmanager.trigger_tool('zoom')
    assert ax.get_navigate_mode() == "ZOOM"
    fig.canvas.manager.toolmanager.trigger_tool('pan')
    assert ax.get_navigate_mode() == "PAN"

