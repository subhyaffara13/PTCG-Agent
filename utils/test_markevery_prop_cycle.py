
def test_markevery_prop_cycle(fig_test, fig_ref):
    """Test that we can set markevery prop_cycle."""
    cases = [None, 8, (30, 8), [16, 24, 30], [0, -1],
             slice(100, 200, 3), 0.1, 0.3, 1.5,
             (0.0, 0.1), (0.45, 0.1)]

    cmap = mpl.colormaps['jet']
    colors = cmap(np.linspace(0.2, 0.8, len(cases)))

    x = np.linspace(-1, 1)
    y = 5 * x**2

    axs = fig_ref.add_subplot()
    for i, markevery in enumerate(cases):
        axs.plot(y - i, 'o-', markevery=markevery, color=colors[i])

    matplotlib.rcParams['axes.prop_cycle'] = cycler(markevery=cases,
                                                    color=colors)

    ax = fig_test.add_subplot()
    for i, _ in enumerate(cases):
        ax.plot(y - i, 'o-')

