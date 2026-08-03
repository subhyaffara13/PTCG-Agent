import random

def test_selfloop(graph_constructor):
    # Simple test for graphs with selfloops
    g1 = graph_constructor([(0, 1), (0, 2), (1, 2), (1, 3), (2, 2), (2, 4)])
    nodes = range(5)
    rng = random.Random(42)

    for _ in range(3):
        new_nodes = list(nodes)
        rng.shuffle(new_nodes)
        d = dict(zip(nodes, new_nodes))
        g2 = nx.relabel_nodes(g1, d)
        assert iso.ISMAGS(g1, g2).is_isomorphic()


def test_selfloop():
    # Simple test for graphs with selfloops
    edges = [
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 3),
        (2, 2),
        (2, 4),
        (3, 1),
        (3, 2),
        (4, 2),
        (4, 5),
        (5, 4),
    ]
    nodes = list(range(6))

    rng = random.Random(42)

    for g1 in [nx.Graph(), nx.DiGraph()]:
        g1.add_edges_from(edges)
        for _ in range(100):
            new_nodes = list(nodes)
            rng.shuffle(new_nodes)
            d = dict(zip(nodes, new_nodes))
            g2 = nx.relabel_nodes(g1, d)
            if not g1.is_directed():
                gm = iso.GraphMatcher(g1, g2)
            else:
                gm = iso.DiGraphMatcher(g1, g2)
            assert gm.is_isomorphic()

