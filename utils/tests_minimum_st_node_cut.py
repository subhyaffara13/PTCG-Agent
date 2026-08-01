
def tests_minimum_st_node_cut():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 7, 8, 11, 12])
    G.add_edges_from([(7, 11), (1, 11), (1, 12), (12, 8), (0, 1)])
    nodelist = minimum_st_node_cut(G, 7, 11)
    assert nodelist == set()

