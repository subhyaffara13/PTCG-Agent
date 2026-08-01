
def test_raises_networkx_unbounded():
    with pytest.raises(nx.NetworkXUnbounded):
        raise nx.NetworkXUnbounded

