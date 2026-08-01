
def test_get_figure():
    fig = plt.figure()
    sfig1 = fig.subfigures()
    sfig2 = sfig1.subfigures()
    ax = sfig2.subplots()

    assert fig.get_figure(root=True) is fig
    assert fig.get_figure(root=False) is fig

    assert ax.get_figure() is sfig2
    assert ax.get_figure(root=False) is sfig2
    assert ax.get_figure(root=True) is fig

    # SubFigure.get_figure has separate implementation but should give consistent
    # results to other artists.
    assert sfig2.get_figure(root=False) is sfig1
    assert sfig2.get_figure(root=True) is fig
    # Currently different results by default.
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        assert sfig2.get_figure() is fig
    # No deprecation warning if root and parent figure are the same.
    assert sfig1.get_figure() is fig

    # An artist not yet attached to anything has no figure.
    ln = mlines.Line2D([], [])
    assert ln.get_figure(root=True) is None
    assert ln.get_figure(root=False) is None

    # figure attribute is root for (Sub)Figures but parent for other artists.
    assert ax.figure is sfig2
    assert fig.figure is fig
    assert sfig2.figure is fig

