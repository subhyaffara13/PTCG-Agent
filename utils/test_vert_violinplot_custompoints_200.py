
def test_vert_violinplot_custompoints_200():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(17))
    np.random.seed(123105625)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=False, showextrema=False,
                  showmedians=False, points=200)

