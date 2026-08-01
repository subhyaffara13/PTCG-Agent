
def test_hist_step_empty():
    # From #3886: creating hist from empty dataset raises ValueError
    ax = plt.gca()
    ax.hist([], histtype='step')

