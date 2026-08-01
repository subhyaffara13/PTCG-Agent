
def chvatal_graph(create_using=None):
    """
    Returns the Chvátal Graph

    The Chvátal Graph is an undirected graph with 12 nodes and 24 edges [1]_.
    It has 370 distinct (directed) Hamiltonian cycles, giving a unique generalized
    LCF notation of order 4, two of order 6 , and 43 of order 1 [2]_.

    Parameters
    ----------
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    G : networkx Graph
        The Chvátal graph with 12 nodes and 24 edges

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Chv%C3%A1tal_graph
    .. [2] https://mathworld.wolfram.com/ChvatalGraph.html

    """
    G = nx.from_dict_of_lists(
        {
            0: [1, 4, 6, 9],
            1: [2, 5, 7],
            2: [3, 6, 8],
            3: [4, 7, 9],
            4: [5, 8],
            5: [10, 11],
            6: [10, 11],
            7: [8, 11],
            8: [10],
            9: [10, 11],
        },
        create_using=create_using,
    )
    G.name = "Chvatal Graph"
    return G

