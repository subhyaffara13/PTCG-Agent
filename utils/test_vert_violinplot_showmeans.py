
def test_vert_violinplot_showmeans():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(3))
    np.random.seed(732050807)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=True, showextrema=False,
                  showmedians=False)

