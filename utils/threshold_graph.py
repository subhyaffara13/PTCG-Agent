
def threshold_graph(creation_sequence, create_using=None):
    """
    Create a threshold graph from the creation sequence or compact
    creation_sequence.

    The input sequence can be a

    creation sequence (e.g. ['d','i','d','d','d','i'])
    labeled creation sequence (e.g. [(0,'d'),(2,'d'),(1,'i')])
    compact creation sequence (e.g. [2,1,1,2,0])

    Use cs=creation_sequence(degree_sequence,labeled=True)
    to convert a degree sequence to a creation sequence.

    Returns None if the sequence is not valid
    """
    # Turn input sequence into a labeled creation sequence
    first = creation_sequence[0]
    if isinstance(first, str):  # creation sequence
        ci = list(enumerate(creation_sequence))
    elif isinstance(first, tuple):  # labeled creation sequence
        ci = creation_sequence[:]
    elif isinstance(first, int):  # compact creation sequence
        cs = uncompact(creation_sequence)
        ci = list(enumerate(cs))
    else:
        raise ValueError("not a valid creation sequence")

    G = nx.empty_graph(0, create_using)
    if G.is_directed():
        raise nx.NetworkXError("Directed Graph not supported")

    G.name = "Threshold Graph"

    # add nodes and edges
    # if type is 'i' just add nodea
    # if type is a d connect to everything previous
    while ci:
        (v, node_type) = ci.pop(0)
        if node_type == "d":  # dominating type, connect to all existing nodes
            # We use `for u in list(G):` instead of
            # `for u in G:` because we edit the graph `G` in
            # the loop. Hence using an iterator will result in
            # `RuntimeError: dictionary changed size during iteration`
            for u in list(G):
                G.add_edge(v, u)
        G.add_node(v)
    return G

