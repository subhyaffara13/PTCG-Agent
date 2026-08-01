
def test_legend_labelcolor_linecolor_histograms():
    x = np.arange(10)

    # testing c kwarg for bar, step, and stepfilled histograms
    fig, ax = plt.subplots()
    h = ax.hist(x, histtype='bar', color='r', label="red bar hist with a red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'r', facecolor=True)

    h = ax.hist(x, histtype='step', color='g', label="green step hist, green label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'g', edgecolor=True)

    h = ax.hist(x, histtype='stepfilled', color='b',
                label="blue stepfilled hist with a blue label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'b', facecolor=True)

    # testing c, fc, and ec combinations for bar histograms
    h = ax.hist(x, histtype='bar', color='r', ec='b',
                label="red bar hist with blue edges and a red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'r', facecolor=True)

    h = ax.hist(x, histtype='bar', fc='r', ec='b',
                label="red bar hist with blue edges and a red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'r', facecolor=True)

    h = ax.hist(x, histtype='bar', fc='none', ec='b',
                label="unfilled blue bar hist with a blue label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'b', edgecolor=True)

    # testing c, and ec combinations for step histograms
    h = ax.hist(x, histtype='step', color='r', ec='b',
                label="blue step hist with a blue label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'b', edgecolor=True)

    h = ax.hist(x, histtype='step', ec='b',
                label="blue step hist with a blue label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'b', edgecolor=True)

    # testing c, fc, and ec combinations for stepfilled histograms
    h = ax.hist(x, histtype='stepfilled', color='r', ec='b',
                label="red stepfilled hist, blue edges, red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'r', facecolor=True)

    h = ax.hist(x, histtype='stepfilled', fc='r', ec='b',
                label="red stepfilled hist, blue edges, red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'r', facecolor=True)

    h = ax.hist(x, histtype='stepfilled', fc='none', ec='b',
                label="unfilled blue stepfilled hist, blue label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'b', edgecolor=True)

    h = ax.hist(x, histtype='stepfilled', fc='r', ec='none',
                label="edgeless red stepfilled hist with a red label")
    leg = ax.legend(labelcolor='linecolor')
    assert_last_legend_patch_color(h, leg, 'r', facecolor=True)

