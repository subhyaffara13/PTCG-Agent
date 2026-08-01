
def test_child_axes_removal():
    fig, ax = plt.subplots()
    marginal = ax.inset_axes([1, 0, .1, 1], sharey=ax)
    marginal_twin = marginal.twinx()
    marginal.remove()
    ax.set(xlim=(-1, 1), ylim=(10, 20))

