
def test_raises_networkx_unfeasible():
    with pytest.raises(nx.NetworkXUnfeasible):
        raise nx.NetworkXUnfeasible

