
def _two_sweep_directed(G, seed):
    """Helper function for finding a lower bound on the diameter
        for directed Graphs.

        It implements 2-dSweep, the directed version of the 2-sweep algorithm.
        The algorithm follows the following steps.
        1. Select a source node $s$ at random.
        2. Perform a forward BFS from $s$ to select a node $a_1$ at the maximum
        distance from the source, and compute $LB_1$, the backward eccentricity of $a_1$.
        3. Perform a backward BFS from $s$ to select a node $a_2$ at the maximum
        distance from the source, and compute $LB_2$, the forward eccentricity of $a_2$.
        4. Return the maximum between $LB_1$ and $LB_2$.

        ``G`` is a NetworkX directed graph.

    .. note::

        ``seed`` is a random.Random or numpy.random.RandomState instance
    """
    # get a new digraph G' with the edges reversed in the opposite direction
    G_reversed = G.reverse()
    # select a random source node
    source = seed.choice(list(G))
    # compute forward distances from source
    forward_distances = nx.shortest_path_length(G, source)
    # compute backward distances  from source
    backward_distances = nx.shortest_path_length(G_reversed, source)
    # if either the source can't reach every node or not every node
    # can reach the source, then the graph is not strongly connected
    n = len(G)
    if len(forward_distances) != n or len(backward_distances) != n:
        raise nx.NetworkXError("DiGraph not strongly connected.")
    # take a node a_1 at the maximum distance from the source in G
    *_, a_1 = forward_distances
    # take a node a_2 at the maximum distance from the source in G_reversed
    *_, a_2 = backward_distances
    # return the max between the backward eccentricity of a_1 and the forward eccentricity of a_2
    return max(nx.eccentricity(G_reversed, a_1), nx.eccentricity(G, a_2))

