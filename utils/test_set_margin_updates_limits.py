
def test_set_margin_updates_limits():
    mpl.style.use("default")
    fig, ax = plt.subplots()
    ax.plot([1, 2], [1, 2])
    ax.set(xscale="log", xmargin=0)
    assert ax.get_xlim() == (1, 2)

