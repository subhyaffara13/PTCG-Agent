
def test_vert_violinplot_showall():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(11))
    np.random.seed(316624790)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=True, showextrema=True,
                  showmedians=True,
                  quantiles=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]])

