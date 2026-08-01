
def test_text_stale():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    plt.draw_all()
    assert not ax1.stale
    assert not ax2.stale
    assert not fig.stale

    txt1 = ax1.text(.5, .5, 'aardvark')
    assert ax1.stale
    assert txt1.stale
    assert fig.stale

    ann1 = ax2.annotate('aardvark', xy=[.5, .5])
    assert ax2.stale
    assert ann1.stale
    assert fig.stale

    plt.draw_all()
    assert not ax1.stale
    assert not ax2.stale
    assert not fig.stale

