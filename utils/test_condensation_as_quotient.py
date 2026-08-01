
def test_condensation_as_quotient():
    """This tests that the condensation of a graph can be viewed as the
    quotient graph under the "in the same connected component" equivalence
    relation.

    """
    # This example graph comes from the file `test_strongly_connected.py`.
    G = nx.DiGraph()
    G.add_edges_from(
        [
            (1, 2),
            (2, 3),
            (2, 11),
            (2, 12),
            (3, 4),
            (4, 3),
            (4, 5),
            (5, 6),
            (6, 5),
            (6, 7),
            (7, 8),
            (7, 9),
            (7, 10),
            (8, 9),
            (9, 7),
            (10, 6),
            (11, 2),
            (11, 4),
            (11, 6),
            (12, 6),
            (12, 11),
        ]
    )
    scc = list(nx.strongly_connected_components(G))
    C = nx.condensation(G, scc)
    component_of = C.graph["mapping"]
    # Two nodes are equivalent if they are in the same connected component.

    def same_component(u, v):
        return component_of[u] == component_of[v]

    Q = nx.quotient_graph(G, same_component)
    assert nx.is_isomorphic(C, Q)

