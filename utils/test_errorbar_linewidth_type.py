
def test_errorbar_linewidth_type(elinewidth):
    plt.errorbar([1, 2, 3], [1, 2, 3], yerr=[1, 2, 3], elinewidth=elinewidth)

