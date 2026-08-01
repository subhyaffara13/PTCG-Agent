
def test_boxplot_no_weird_whisker():
    x = np.array([3, 9000, 150, 88, 350, 200000, 1400, 960],
                 dtype=np.float64)
    ax1 = plt.axes()
    ax1.boxplot(x)
    ax1.set_yscale('log')
    ax1.yaxis.grid(False, which='minor')
    ax1.xaxis.grid(False)

