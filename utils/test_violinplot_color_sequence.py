
def test_violinplot_color_sequence():
    # Ensures that setting a sequence of colors works the same as setting
    # each color independently
    np.random.seed(19680801)
    data = [sorted(np.random.normal(0, std, 100)) for std in range(1, 5)]
    kwargs = {'showmeans': True, 'showextrema': True, 'showmedians': True}

    def assert_colors_equal(colors1, colors2):
        assert all(mcolors.same_color(c1, c2)
                   for c1, c2 in zip(colors1, colors2))

    # Color sequence
    N = len(data)
    positions = range(N)
    facecolors = ['k', 'r', ('b', 0.5), ('g', 0.2)]
    linecolors = [('y', 0.4), 'b', 'm', ('k', 0.8)]

    # Test image
    fig_test = plt.figure()
    ax = fig_test.gca()
    parts_test = ax.violinplot(data,
                               positions=positions,
                               facecolor=facecolors,
                               linecolor=linecolors,
                               **kwargs)

    body_colors = [p.get_facecolor() for p in parts_test["bodies"]]
    assert_colors_equal(body_colors, mcolors.to_rgba_array(facecolors))

    for part in ["cbars", "cmins", "cmaxes", "cmeans", "cmedians"]:
        colors_test = parts_test[part].get_edgecolor()
        assert_colors_equal(colors_test, mcolors.to_rgba_array(linecolors))

