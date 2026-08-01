
def test_piecontainer_remove():
    fig, ax = plt.subplots()
    pie = ax.pie([2, 3], labels=['foo', 'bar'], autopct="%1.0f%%")
    ax.pie_label(pie, ['baz', 'qux'])
    assert len(ax.patches) == 2
    assert len(ax.texts) == 6

    pie.remove()
    assert not ax.patches
    assert not ax.texts

