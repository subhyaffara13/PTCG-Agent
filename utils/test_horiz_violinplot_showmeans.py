
def test_horiz_violinplot_showmeans():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(29))
    np.random.seed(385164807)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=True,
                  showextrema=False, showmedians=False)

