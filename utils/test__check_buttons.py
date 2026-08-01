
def test_CheckButtons(ax):
    labels = ('a', 'b', 'c')
    check = widgets.CheckButtons(ax, labels, (True, False, True))
    assert check.get_status() == [True, False, True]
    check.set_active(0)
    assert check.get_status() == [False, False, True]
    assert check.get_checked_labels() == ['c']
    check.clear()
    assert check.get_status() == [False, False, False]
    assert check.get_checked_labels() == []

    for invalid_index in [-1, len(labels), len(labels)+5]:
        with pytest.raises(ValueError):
            check.set_active(index=invalid_index)

    for invalid_value in ['invalid', -1]:
        with pytest.raises(TypeError):
            check.set_active(1, state=invalid_value)

    cid = check.on_clicked(lambda: None)
    check.disconnect(cid)

