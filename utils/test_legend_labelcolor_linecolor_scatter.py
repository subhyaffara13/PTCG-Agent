
def test_legend_labelcolor_linecolor_scatter():
    x = np.arange(5)

    # testing c, fc, and ec combinations for scatter plots
    fig, ax = plt.subplots()
    s = ax.scatter(x, x, c='r', label="red circles with a red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_scattermarker_color(s, leg, 'r', facecolor=True)

    s = ax.scatter(x, x, c='r', ec='b', label="red circles, blue edges, red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_scattermarker_color(s, leg, 'r', facecolor=True)

    s = ax.scatter(x, x, fc='r', ec='b', label="red circles, blue edges, red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_scattermarker_color(s, leg, 'r', facecolor=True)

    # 'none' cases
    s = ax.scatter(x, x, fc='none', ec='b', label="blue unfilled circles, blue label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_scattermarker_color(s, leg, 'b', edgecolor=True)

    s = ax.scatter(x, x, fc='r', ec='none', label="red edgeless circles, red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_scattermarker_color(s, leg, 'r', facecolor=True)

    s = ax.scatter(x, x, c='none', ec='none',
                   label="black label despite invisible circles for dummy entries")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_scattermarker_color(s, leg, 'k')

