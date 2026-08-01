
def test_plot_format():
    fig, ax = plt.subplots()
    line = ax.plot([1, 2, 3], '1.0')
    assert line[0].get_color() == (1.0, 1.0, 1.0, 1.0)
    assert line[0].get_marker() == 'None'
    fig, ax = plt.subplots()
    line = ax.plot([1, 2, 3], '1')
    assert line[0].get_marker() == '1'
    fig, ax = plt.subplots()
    line = ax.plot([1, 2], [1, 2], '1.0', "1")
    fig.canvas.draw()
    assert line[0].get_color() == (1.0, 1.0, 1.0, 1.0)
    assert ax.get_yticklabels()[0].get_text() == '1'
    fig, ax = plt.subplots()
    line = ax.plot([1, 2], [1, 2], '1', "1.0")
    fig.canvas.draw()
    assert line[0].get_marker() == '1'
    assert ax.get_yticklabels()[0].get_text() == '1.0'
    fig, ax = plt.subplots()
    line = ax.plot([1, 2, 3], 'k3')
    assert line[0].get_marker() == '3'
    assert line[0].get_color() == 'k'
    fig, ax = plt.subplots()
    line = ax.plot([1, 2, 3], '.C12:')
    assert line[0].get_marker() == '.'
    assert line[0].get_color() == mcolors.to_rgba('C12')
    assert line[0].get_linestyle() == ':'

