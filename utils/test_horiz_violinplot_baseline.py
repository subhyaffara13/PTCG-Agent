
def test_horiz_violinplot_baseline():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(19))
    np.random.seed(358898943)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=False,
                  showextrema=False, showmedians=False)

