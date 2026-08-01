
def test_legend_labelcolor_linecolor_plot():
    x = np.arange(5)

    # testing line plot
    fig, ax = plt.subplots()
    l, = ax.plot(x, c='r', label="red line with a red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_linemarker_color(l, leg, 'r', color=True)

    # testing c, fc, and ec combinations for maker plots
    l, = ax.plot(x, 'o', c='r', label="red circles with a red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_linemarker_color(l, leg, 'r', color=True)

    l, = ax.plot(x, 'o', c='r', mec='b', label="red circles, blue edges, red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_linemarker_color(l, leg, 'r', color=True)

    l, = ax.plot(x, 'o', mfc='r', mec='b', label="red circles, blue edges, red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_linemarker_color(l, leg, 'r', facecolor=True)

    # 'none' cases
    l, = ax.plot(x, 'o', mfc='none', mec='b',
                 label="blue unfilled circles, blue label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_linemarker_color(l, leg, 'b', edgecolor=True)

    l, = ax.plot(x, 'o', mfc='r', mec='none', label="red edgeless circles, red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_linemarker_color(l, leg, 'r', facecolor=True)

    l, = ax.plot(x, 'o', c='none', mec='none',
                 label="black label despite invisible circles for dummy entries")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_linemarker_color(l, leg, 'k')

