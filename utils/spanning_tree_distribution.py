
def spanning_tree_distribution(G, z):
    """
    Find the asadpour exponential distribution of spanning trees.

    Solves the Maximum Entropy Convex Program in the Asadpour algorithm [1]_
    using the approach in section 7 to build an exponential distribution of
    undirected spanning trees.

    This algorithm ensures that the probability of any edge in a spanning
    tree is proportional to the sum of the probabilities of the tress
    containing that edge over the sum of the probabilities of all spanning
    trees of the graph.

    Parameters
    ----------
    G : nx.MultiGraph
        The undirected support graph for the Held Karp relaxation

    z : dict
        The output of `held_karp_ascent()`, a scaled version of the Held-Karp
        solution.

    Returns
    -------
    gamma : dict
        The probability distribution which approximately preserves the marginal
        probabilities of `z`.
    """
    from math import exp
    from math import log as ln

    def q(e):
        """
        The value of q(e) is described in the Asadpour paper is "the
        probability that edge e will be included in a spanning tree T that is
        chosen with probability proportional to exp(gamma(T))" which
        basically means that it is the total probability of the edge appearing
        across the whole distribution.

        Parameters
        ----------
        e : tuple
            The `(u, v)` tuple describing the edge we are interested in

        Returns
        -------
        float
            The probability that a spanning tree chosen according to the
            current values of gamma will include edge `e`.
        """
        # Create the laplacian matrices
        for u, v, d in G.edges(data=True):
            d[lambda_key] = exp(gamma[(u, v)])
        G_Kirchhoff = nx.number_of_spanning_trees(G, weight=lambda_key)
        G_e = nx.contracted_edge(G, e, self_loops=False)
        G_e_Kirchhoff = nx.number_of_spanning_trees(G_e, weight=lambda_key)

        # Multiply by the weight of the contracted edge since it is not included
        # in the total weight of the contracted graph.
        return exp(gamma[(e[0], e[1])]) * G_e_Kirchhoff / G_Kirchhoff

    # initialize gamma to the zero dict
    gamma = {}
    for u, v, _ in G.edges:
        gamma[(u, v)] = 0

    # set epsilon
    EPSILON = 0.2

    # pick an edge attribute name that is unlikely to be in the graph
    lambda_key = "spanning_tree_distribution's secret attribute name for lambda"

    while True:
        # We need to know that know that no values of q_e are greater than
        # (1 + epsilon) * z_e, however changing one gamma value can increase the
        # value of a different q_e, so we have to complete the for loop without
        # changing anything for the condition to be meet
        in_range_count = 0
        # Search for an edge with q_e > (1 + epsilon) * z_e
        for u, v in gamma:
            e = (u, v)
            q_e = q(e)
            z_e = z[e]
            if q_e > (1 + EPSILON) * z_e:
                delta = ln(
                    (q_e * (1 - (1 + EPSILON / 2) * z_e))
                    / ((1 - q_e) * (1 + EPSILON / 2) * z_e)
                )
                gamma[e] -= delta
                # Check that delta had the desired effect
                new_q_e = q(e)
                desired_q_e = (1 + EPSILON / 2) * z_e
                if round(new_q_e, 8) != round(desired_q_e, 8):
                    raise nx.NetworkXError(
                        f"Unable to modify probability for edge ({u}, {v})"
                    )
            else:
                in_range_count += 1
        # Check if the for loop terminated without changing any gamma
        if in_range_count == len(gamma):
            break

    # Remove the new edge attributes
    for _, _, d in G.edges(data=True):
        if lambda_key in d:
            del d[lambda_key]

    return gamma

