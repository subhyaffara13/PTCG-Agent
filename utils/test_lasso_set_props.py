
def test_lasso_set_props(ax):
    onselect = mock.Mock(spec=noop, return_value=None)
    tool = widgets.Lasso(ax, (100, 100), onselect)
    line = tool.line
    assert mcolors.same_color(line.get_color(), 'black')
    assert line.get_linestyle() == '-'
    assert line.get_lw() == 2
    tool = widgets.Lasso(ax, (100, 100), onselect, props=dict(
        linestyle='-', color='darkblue', alpha=0.2, lw=1))

    line = tool.line
    assert mcolors.same_color(line.get_color(), 'darkblue')
    assert line.get_alpha() == 0.2
    assert line.get_lw() == 1
    assert line.get_linestyle() == '-'
    line.set_color('r')
    line.set_alpha(0.3)
    assert mcolors.same_color(line.get_color(), 'r')
    assert line.get_alpha() == 0.3

