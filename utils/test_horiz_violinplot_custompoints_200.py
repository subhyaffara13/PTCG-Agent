
def test_horiz_violinplot_custompoints_200():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(43))
    np.random.seed(557438524)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=False,
                  showextrema=False, showmedians=False, points=200)

