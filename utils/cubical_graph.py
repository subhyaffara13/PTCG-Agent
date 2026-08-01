
def cubical_graph(create_using=None):
    """
    Returns the 3-regular Platonic Cubical Graph

    The skeleton of the cube (the nodes and edges) form a graph, with 8
    nodes, and 12 edges. It is a special case of the hypercube graph.
    It is one of 5 Platonic graphs, each a skeleton of its
    Platonic solid [1]_.
    Such graphs arise in parallel processing in computers.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        A cubical graph with 8 nodes and 12 edges

    See Also
    --------
    tetrahedral_graph, octahedral_graph, dodecahedral_graph, icosahedral_graph

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Cube#Cubical_graph

    """
    G = nx.from_dict_of_lists(
        {
            0: [1, 3, 4],
            1: [0, 2, 7],
            2: [1, 3, 6],
            3: [0, 2, 5],
            4: [0, 5, 7],
            5: [3, 4, 6],
            6: [2, 5, 7],
            7: [1, 4, 6],
        },
        create_using=create_using,
    )
    G.name = "Platonic Cubical Graph"
    return G

