
def test_legend_remove():
    fig, ax = plt.subplots()
    lines = ax.plot(range(10))
    leg = fig.legend(lines, ["test"])
    leg.remove()
    assert fig.legends == []
    leg = ax.legend("test")
    leg.remove()
    assert ax.get_legend() is None

