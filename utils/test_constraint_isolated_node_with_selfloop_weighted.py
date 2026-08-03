import math


def test_constraint_isolated_node_with_selfloop_weighted(graph):
    """Weighted self-loop. See gh-6916"""
    G = graph()
    G.add_weighted_edges_from([(0, 0, 10)])
    assert math.isnan(nx.constraint(G)[0])

