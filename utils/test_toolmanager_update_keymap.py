
def test_toolmanager_update_keymap():
    with pytest.warns(UserWarning, match=_EXPECTED_WARNING_TOOLMANAGER):
        plt.rcParams['toolbar'] = 'toolmanager'
    fig = plt.gcf()
    assert 'v' in fig.canvas.manager.toolmanager.get_tool_keymap('forward')
    with pytest.warns(UserWarning,
                      match="Key c changed from back to forward"):
        fig.canvas.manager.toolmanager.update_keymap('forward', 'c')
    assert fig.canvas.manager.toolmanager.get_tool_keymap('forward') == ['c']
    with pytest.raises(KeyError, match="'foo' not in Tools"):
        fig.canvas.manager.toolmanager.update_keymap('foo', 'c')

