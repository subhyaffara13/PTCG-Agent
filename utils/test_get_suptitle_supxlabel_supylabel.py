
def test_get_suptitle_supxlabel_supylabel():
    fig, ax = plt.subplots()
    assert fig.get_suptitle() == ""
    assert fig.get_supxlabel() == ""
    assert fig.get_supylabel() == ""
    fig.suptitle('suptitle')
    assert fig.get_suptitle() == 'suptitle'
    fig.supxlabel('supxlabel')
    assert fig.get_supxlabel() == 'supxlabel'
    fig.supylabel('supylabel')
    assert fig.get_supylabel() == 'supylabel'

