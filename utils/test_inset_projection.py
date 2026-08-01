
def test_inset_projection():
    _, ax = plt.subplots()
    axins = ax.inset_axes([0.2, 0.2, 0.3, 0.3], projection="hammer")
    assert isinstance(axins, HammerAxes)

