
def test_get_set_draggable():
    legend = plt.legend()
    assert not legend.get_draggable()
    legend.set_draggable(True)
    assert legend.get_draggable()
    legend.set_draggable(False)
    assert not legend.get_draggable()

