
def test_complete():
    """In complete graphs each node is a dominating set.
    Thus the dominating set has to be of cardinality 1.
    """
    K4 = nx.complete_graph(4)
    assert len(nx.dominating_set(K4)) == 1
    K5 = nx.complete_graph(5)
    assert len(nx.dominating_set(K5)) == 1


def test_complete():
    G = nx.complete_graph(5)
    assert average_clustering(G, trials=len(G) // 2) == 1
    G = nx.complete_graph(7)
    assert average_clustering(G, trials=len(G) // 2) == 1


def test_complete(fig_test, fig_ref):
    _generate_complete_test_figure(fig_ref)
    # plotting is done, now test its pickle-ability
    pkl = pickle.dumps(fig_ref, pickle.HIGHEST_PROTOCOL)
    # FigureCanvasAgg is picklable and GUI canvases are generally not, but there should
    # be no reference to the canvas in the pickle stream in either case.  In order to
    # keep the test independent of GUI toolkits, run it with Agg and check that there's
    # no reference to FigureCanvasAgg in the pickle stream.
    assert "FigureCanvasAgg" not in [arg for op, arg, pos in pickletools.genops(pkl)]
    loaded = pickle.loads(pkl)
    loaded.canvas.draw()

    fig_test.set_size_inches(loaded.get_size_inches())
    fig_test.figimage(loaded.canvas.renderer.buffer_rgba())

    plt.close(loaded)

