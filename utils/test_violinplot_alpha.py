
def test_violinplot_alpha():
    matplotlib.style.use('default')
    data = [(np.random.normal(0, 1, 100))]

    fig, ax = plt.subplots()
    parts = ax.violinplot(data, positions=[1])

    # Case 1: If facecolor is unspecified, it's the first color from the color cycle
    # with Artist-level alpha=0.3
    facecolor = ('y' if mpl.rcParams['_internal.classic_mode']
                 else plt.rcParams['axes.prop_cycle'].by_key()['color'][0])
    assert mcolors.same_color(parts['bodies'][0].get_facecolor(), (facecolor, 0.3))
    assert parts['bodies'][0].get_alpha() == 0.3
    # setting a new facecolor maintains the alpha
    parts['bodies'][0].set_facecolor('red')
    assert mcolors.same_color(parts['bodies'][0].get_facecolor(), ('red', 0.3))

    # Case 2: If facecolor is explicitly given, it's alpha does not become an
    # Artist property
    parts = ax.violinplot(data, positions=[1], facecolor=('blue', 0.3))
    assert mcolors.same_color(parts['bodies'][0].get_facecolor(), ('blue', 0.3))
    assert parts['bodies'][0].get_alpha() is None
    # so setting a new color does not maintain the alpha
    parts['bodies'][0].set_facecolor('red')
    assert mcolors.same_color(parts['bodies'][0].get_facecolor(), 'red')

