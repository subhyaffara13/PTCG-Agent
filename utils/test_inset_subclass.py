
def test_inset_subclass():
    _, ax = plt.subplots()
    axins = ax.inset_axes([0.2, 0.2, 0.3, 0.3], axes_class=AA.Axes)
    assert isinstance(axins, AA.Axes)

