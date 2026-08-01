
def chain_and_fork_graph():
    edge_list = [("A", "B"), ("B", "C"), ("B", "D"), ("D", "C")]
    G = nx.DiGraph(edge_list)
    return G

