
def test_stochastic_block_model():
    sizes = [75, 75, 300]
    probs = [[0.25, 0.05, 0.02], [0.05, 0.35, 0.07], [0.02, 0.07, 0.40]]
    G = nx.stochastic_block_model(sizes, probs, seed=0)
    C = G.graph["partition"]
    assert len(C) == 3
    assert len(G) == 450
    assert G.size() == 22160

    GG = nx.stochastic_block_model(sizes, probs, range(450), seed=0)
    assert G.nodes == GG.nodes

    # Test Exceptions
    sbm = nx.stochastic_block_model
    badnodelist = list(range(400))  # not enough nodes to match sizes
    badprobs1 = [[0.25, 0.05, 1.02], [0.05, 0.35, 0.07], [0.02, 0.07, 0.40]]
    badprobs2 = [[0.25, 0.05, 0.02], [0.05, -0.35, 0.07], [0.02, 0.07, 0.40]]
    probs_rect1 = [[0.25, 0.05, 0.02], [0.05, -0.35, 0.07]]
    probs_rect2 = [[0.25, 0.05], [0.05, -0.35], [0.02, 0.07]]
    asymprobs = [[0.25, 0.05, 0.01], [0.05, -0.35, 0.07], [0.02, 0.07, 0.40]]
    pytest.raises(nx.NetworkXException, sbm, sizes, badprobs1)
    pytest.raises(nx.NetworkXException, sbm, sizes, badprobs2)
    pytest.raises(nx.NetworkXException, sbm, sizes, probs_rect1, directed=True)
    pytest.raises(nx.NetworkXException, sbm, sizes, probs_rect2, directed=True)
    pytest.raises(nx.NetworkXException, sbm, sizes, asymprobs, directed=False)
    pytest.raises(nx.NetworkXException, sbm, sizes, probs, badnodelist)
    nodelist = [0] + list(range(449))  # repeated node name in nodelist
    pytest.raises(nx.NetworkXException, sbm, sizes, probs, nodelist)

    # Extra keyword arguments test
    GG = nx.stochastic_block_model(sizes, probs, seed=0, selfloops=True)
    assert G.nodes == GG.nodes
    GG = nx.stochastic_block_model(sizes, probs, selfloops=True, directed=True)
    assert G.nodes == GG.nodes
    GG = nx.stochastic_block_model(sizes, probs, seed=0, sparse=False)
    assert G.nodes == GG.nodes

