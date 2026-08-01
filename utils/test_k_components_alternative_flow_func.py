
def test_k_components_alternative_flow_func(flow_func):
    G = nx.lollipop_graph(5, 5)
    result = nx.k_components(G, flow_func=flow_func)
    _check_connectivity(G, result)

