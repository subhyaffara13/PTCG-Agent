
def test_remove_suptitle_supxlabel_supylabel():
    fig = plt.figure()

    title = fig.suptitle('suptitle')
    xlabel = fig.supxlabel('supxlabel')
    ylabel = fig.supylabel('supylabel')

    assert len(fig.texts) == 3
    assert fig._suptitle is not None
    assert fig._supxlabel is not None
    assert fig._supylabel is not None

    title.remove()
    assert fig._suptitle is None
    xlabel.remove()
    assert fig._supxlabel is None
    ylabel.remove()
    assert fig._supylabel is None

    assert not fig.texts

