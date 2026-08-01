
def test_nonlinear_containment():
    fig, ax = plt.subplots()
    ax.set(xscale="log", ylim=(0, 1))
    polygon = ax.axvspan(1, 10)
    assert polygon.get_path().contains_point(
        ax.transData.transform((5, .5)), polygon.get_transform())
    assert not polygon.get_path().contains_point(
        ax.transData.transform((.5, .5)), polygon.get_transform())
    assert not polygon.get_path().contains_point(
        ax.transData.transform((50, .5)), polygon.get_transform())

