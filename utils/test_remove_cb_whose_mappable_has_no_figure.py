
def test_remove_cb_whose_mappable_has_no_figure():
    fig, ax = plt.subplots()
    assert fig.get_axes() != []
    cb = fig.colorbar(cm.ScalarMappable(), cax=ax)
    cb.remove()
    assert fig.get_axes() == []

