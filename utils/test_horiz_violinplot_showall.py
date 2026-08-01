
def test_horiz_violinplot_showall():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(37))
    np.random.seed(82762530)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=True,
                  showextrema=True, showmedians=True,
                  quantiles=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]])

