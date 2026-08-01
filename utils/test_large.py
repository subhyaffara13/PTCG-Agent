
def test_large():
    s = pd.Series([range(256)]).explode()
    result = s.explode()
    tm.assert_series_equal(result, s)


def test_large():
    fname = (
        importlib.resources.files("networkx.algorithms.flow.tests")
        / "netgen-2.gpickle.bz2"
    )

    with bz2.BZ2File(fname, "rb") as f:
        G = pickle.load(f)
    flowCost, flowDict = nx.network_simplex(G)
    assert 6749969302 == flowCost
    assert 6749969302 == nx.cost_of_flow(G, flowDict)

