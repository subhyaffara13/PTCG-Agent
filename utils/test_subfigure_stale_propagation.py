
def test_subfigure_stale_propagation():
    fig = plt.figure()

    fig.draw_without_rendering()
    assert not fig.stale

    sfig1 = fig.subfigures()
    assert fig.stale

    fig.draw_without_rendering()
    assert not fig.stale
    assert not sfig1.stale

    sfig2 = sfig1.subfigures()
    assert fig.stale
    assert sfig1.stale

    fig.draw_without_rendering()
    assert not fig.stale
    assert not sfig1.stale
    assert not sfig2.stale

    sfig2.stale = True
    assert sfig1.stale
    assert fig.stale

