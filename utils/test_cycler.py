
def test_cycler():
    ax = plt.figure().add_subplot()
    ax.set_prop_cycle(c=["c", "m", "y", "k"])
    ax.plot([1, 2])
    ax = pickle.loads(pickle.dumps(ax))
    l, = ax.plot([3, 4])
    assert l.get_color() == "m"

