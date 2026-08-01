
def test_figure_legend_outside():
    todos = ['upper ' + pos for pos in ['left', 'center', 'right']]
    todos += ['lower ' + pos for pos in ['left', 'center', 'right']]
    todos += ['left ' + pos for pos in ['lower', 'center', 'upper']]
    todos += ['right ' + pos for pos in ['lower', 'center', 'upper']]

    upperext = [20.722556, 26.389222, 790.333, 545.16762]
    lowerext = [20.722556, 70.723222, 790.333, 589.50162]
    leftext = [152.056556, 26.389222, 790.333, 589.50162]
    rightext = [20.722556, 26.389222, 658.999, 589.50162]
    axbb = [upperext, upperext, upperext,
            lowerext, lowerext, lowerext,
            leftext, leftext, leftext,
            rightext, rightext, rightext]

    legbb = [[10., 554., 133., 590.],     # upper left
             [338.5, 554., 461.5, 590.],  # upper center
             [667, 554., 790.,  590.],    # upper right
             [10., 10., 133.,  46.],      # lower left
             [338.5, 10., 461.5,  46.],   # lower center
             [667., 10., 790.,  46.],     # lower right
             [10., 10., 133., 46.],       # left lower
             [10., 282., 133., 318.],     # left center
             [10., 554., 133., 590.],     # left upper
             [667, 10., 790., 46.],       # right lower
             [667., 282., 790., 318.],    # right center
             [667., 554., 790., 590.]]    # right upper

    for nn, todo in enumerate(todos):
        print(todo)
        fig, axs = plt.subplots(constrained_layout=True, dpi=100)
        axs.plot(range(10), label='Boo1')
        leg = fig.legend(loc='outside ' + todo)
        fig.draw_without_rendering()

        assert_allclose(axs.get_window_extent().extents, axbb[nn],
                        rtol=1e-4)
        assert_allclose(leg.get_window_extent().extents, legbb[nn],
                        rtol=1e-4)

