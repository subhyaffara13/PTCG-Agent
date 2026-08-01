
def test_axes(subplots):
    fig, ax = subplots
    nx.draw(barbell, ax=ax)
    nx.draw_networkx_edge_labels(barbell, nx.circular_layout(barbell), ax=ax)


def test_axes():
    try:
        import matplotlib
        version = matplotlib.__version__.split("-")[0]
        version = version.split(".")[:2]
        if [int(_) for _ in version] < [0,99]:
            raise ImportError
        import pylab
    except ImportError:
        print("\nSkipping test (pylab not available or too old version)\n")
        return
    fig = pylab.figure()
    axes = fig.add_subplot(111)
    for ctx in [mp, fp]:
        ctx.plot(lambda x: x**2, [0, 3], axes=axes)
        assert axes.get_xlabel() == 'x'
        assert axes.get_ylabel() == 'f(x)'

    fig = pylab.figure()
    axes = fig.add_subplot(111)
    for ctx in [mp, fp]:
        ctx.cplot(lambda z: z, [-2, 2], [-10, 10], axes=axes)
    assert axes.get_xlabel() == 'Re(z)'
    assert axes.get_ylabel() == 'Im(z)'

