
def test_figure_clear(clear_meth):
    # we test the following figure clearing scenarios:
    fig = plt.figure()

    # a) an empty figure
    fig.clear()
    assert fig.axes == []

    # b) a figure with a single unnested axes
    ax = fig.add_subplot(111)
    getattr(fig, clear_meth)()
    assert fig.axes == []

    # c) a figure multiple unnested axes
    axes = [fig.add_subplot(2, 1, i+1) for i in range(2)]
    getattr(fig, clear_meth)()
    assert fig.axes == []

    # d) a figure with a subfigure
    gs = fig.add_gridspec(ncols=2, nrows=1)
    subfig = fig.add_subfigure(gs[0])
    subaxes = subfig.add_subplot(111)
    getattr(fig, clear_meth)()
    assert subfig not in fig.subfigs
    assert fig.axes == []

    # e) a figure with a subfigure and a subplot
    subfig = fig.add_subfigure(gs[0])
    subaxes = subfig.add_subplot(111)
    mainaxes = fig.add_subplot(gs[1])

    # e.1) removing just the axes leaves the subplot
    mainaxes.remove()
    assert fig.axes == [subaxes]

    # e.2) removing just the subaxes leaves the subplot
    # and subfigure
    mainaxes = fig.add_subplot(gs[1])
    subaxes.remove()
    assert fig.axes == [mainaxes]
    assert subfig in fig.subfigs

    # e.3) clearing the subfigure leaves the subplot
    subaxes = subfig.add_subplot(111)
    assert mainaxes in fig.axes
    assert subaxes in fig.axes
    getattr(subfig, clear_meth)()
    assert subfig in fig.subfigs
    assert subaxes not in subfig.axes
    assert subaxes not in fig.axes
    assert mainaxes in fig.axes

    # e.4) clearing the whole thing
    subaxes = subfig.add_subplot(111)
    getattr(fig, clear_meth)()
    assert fig.axes == []
    assert fig.subfigs == []

    # f) multiple subfigures
    subfigs = [fig.add_subfigure(gs[i]) for i in [0, 1]]
    subaxes = [sfig.add_subplot(111) for sfig in subfigs]
    assert all(ax in fig.axes for ax in subaxes)
    assert all(sfig in fig.subfigs for sfig in subfigs)

    # f.1) clearing only one subfigure
    getattr(subfigs[0], clear_meth)()
    assert subaxes[0] not in fig.axes
    assert subaxes[1] in fig.axes
    assert subfigs[1] in fig.subfigs

    # f.2) clearing the whole thing
    getattr(subfigs[1], clear_meth)()
    subfigs = [fig.add_subfigure(gs[i]) for i in [0, 1]]
    subaxes = [sfig.add_subplot(111) for sfig in subfigs]
    assert all(ax in fig.axes for ax in subaxes)
    assert all(sfig in fig.subfigs for sfig in subfigs)
    getattr(fig, clear_meth)()
    assert fig.subfigs == []
    assert fig.axes == []

