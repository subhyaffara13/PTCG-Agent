
def test_violinplot_sides():
    ax = plt.axes()
    np.random.seed(19680801)
    data = [np.random.normal(size=100)]
    # Check horizontal violinplot
    for pos, side in zip([0, -0.5, 0.5], ['both', 'low', 'high']):
        ax.violinplot(data, positions=[pos], orientation='horizontal', showmeans=False,
                      showextrema=True, showmedians=True, side=side)
    # Check vertical violinplot
    for pos, side in zip([4, 3.5, 4.5], ['both', 'low', 'high']):
        ax.violinplot(data, positions=[pos], orientation='vertical', showmeans=False,
                      showextrema=True, showmedians=True, side=side)

