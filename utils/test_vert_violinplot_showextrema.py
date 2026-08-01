
def test_vert_violinplot_showextrema():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(5))
    np.random.seed(236067977)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=False, showextrema=True,
                  showmedians=False)

