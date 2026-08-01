
def held_karp_ascent(G, weight="weight"):
    """
    Minimizes the Held-Karp relaxation of the TSP for `G`

    Solves the Held-Karp relaxation of the input complete digraph and scales
    the output solution for use in the Asadpour [1]_ ASTP algorithm.

    The Held-Karp relaxation defines the lower bound for solutions to the
    ATSP, although it does return a fractional solution. This is used in the
    Asadpour algorithm as an initial solution which is later rounded to a
    integral tree within the spanning tree polytopes. This function solves
    the relaxation with the branch and bound method in [2]_.

    Parameters
    ----------
    G : nx.DiGraph
        The graph should be a complete weighted directed graph.
        The distance between all paris of nodes should be included.

    weight : string, optional (default="weight")
        Edge data key corresponding to the edge weight.
        If any edge does not have this attribute the weight is set to 1.

    Returns
    -------
    OPT : float
        The cost for the optimal solution to the Held-Karp relaxation
    z : dict or nx.Graph
        A symmetrized and scaled version of the optimal solution to the
        Held-Karp relaxation for use in the Asadpour algorithm.

        If an integral solution is found, then that is an optimal solution for
        the ATSP problem and that is returned instead.

    References
    ----------
    .. [1] A. Asadpour, M. X. Goemans, A. Madry, S. O. Gharan, and A. Saberi,
       An o(log n/log log n)-approximation algorithm for the asymmetric
       traveling salesman problem, Operations research, 65 (2017),
       pp. 1043–1061

    .. [2] M. Held, R. M. Karp, The traveling-salesman problem and minimum
           spanning trees, Operations Research, 1970-11-01, Vol. 18 (6),
           pp.1138-1162
    """
    import numpy as np
    import scipy as sp

    def k_pi():
        """
        Find the set of minimum 1-Arborescences for G at point pi.

        Returns
        -------
        Set
            The set of minimum 1-Arborescences
        """
        # Create a copy of G without vertex 1.
        G_1 = G.copy()
        minimum_1_arborescences = set()
        minimum_1_arborescence_weight = math.inf

        # node is node '1' in the Held and Karp paper
        n = next(G.__iter__())
        G_1.remove_node(n)

        # Iterate over the spanning arborescences of the graph until we know
        # that we have found the minimum 1-arborescences. My proposed strategy
        # is to find the most extensive root to connect to from 'node 1' and
        # the least expensive one. We then iterate over arborescences until
        # the cost of the basic arborescence is the cost of the minimum one
        # plus the difference between the most and least expensive roots,
        # that way the cost of connecting 'node 1' will by definition not by
        # minimum
        min_root = {"node": None, weight: math.inf}
        max_root = {"node": None, weight: -math.inf}
        for u, v, d in G.edges(n, data=True):
            if d[weight] < min_root[weight]:
                min_root = {"node": v, weight: d[weight]}
            if d[weight] > max_root[weight]:
                max_root = {"node": v, weight: d[weight]}

        min_in_edge = min(G.in_edges(n, data=True), key=lambda x: x[2][weight])
        min_root[weight] = min_root[weight] + min_in_edge[2][weight]
        max_root[weight] = max_root[weight] + min_in_edge[2][weight]

        min_arb_weight = math.inf
        for arb in nx.ArborescenceIterator(G_1):
            arb_weight = arb.size(weight)
            if min_arb_weight == math.inf:
                min_arb_weight = arb_weight
            elif arb_weight > min_arb_weight + max_root[weight] - min_root[weight]:
                break
            # We have to pick the root node of the arborescence for the out
            # edge of the first vertex as that is the only node without an
            # edge directed into it.
            for N, deg in arb.in_degree:
                if deg == 0:
                    # root found
                    arb.add_edge(n, N, **{weight: G[n][N][weight]})
                    arb_weight += G[n][N][weight]
                    break

            # We can pick the minimum weight in-edge for the vertex with
            # a cycle. If there are multiple edges with the same, minimum
            # weight, We need to add all of them.
            #
            # Delete the edge (N, v) so that we cannot pick it.
            edge_data = G[N][n]
            G.remove_edge(N, n)
            min_weight = min(G.in_edges(n, data=weight), key=lambda x: x[2])[2]
            min_edges = [
                (u, v, d) for u, v, d in G.in_edges(n, data=weight) if d == min_weight
            ]
            for u, v, d in min_edges:
                new_arb = arb.copy()
                new_arb.add_edge(u, v, **{weight: d})
                new_arb_weight = arb_weight + d
                # Check to see the weight of the arborescence, if it is a
                # new minimum, clear all of the old potential minimum
                # 1-arborescences and add this is the only one. If its
                # weight is above the known minimum, do not add it.
                if new_arb_weight < minimum_1_arborescence_weight:
                    minimum_1_arborescences.clear()
                    minimum_1_arborescence_weight = new_arb_weight
                # We have a 1-arborescence, add it to the set
                if new_arb_weight == minimum_1_arborescence_weight:
                    minimum_1_arborescences.add(new_arb)
            G.add_edge(N, n, **edge_data)

        return minimum_1_arborescences

    def direction_of_ascent():
        """
        Find the direction of ascent at point pi.

        See [1]_ for more information.

        Returns
        -------
        dict
            A mapping from the nodes of the graph which represents the direction
            of ascent.

        References
        ----------
        .. [1] M. Held, R. M. Karp, The traveling-salesman problem and minimum
           spanning trees, Operations Research, 1970-11-01, Vol. 18 (6),
           pp.1138-1162
        """
        # 1. Set d equal to the zero n-vector.
        d = {}
        for n in G:
            d[n] = 0
        del n
        # 2. Find a 1-Arborescence T^k such that k is in K(pi, d).
        minimum_1_arborescences = k_pi()
        while True:
            # Reduce K(pi) to K(pi, d)
            # Find the arborescence in K(pi) which increases the lest in
            # direction d
            min_k_d_weight = math.inf
            min_k_d = None
            for arborescence in minimum_1_arborescences:
                weighted_cost = 0
                for n, deg in arborescence.degree:
                    weighted_cost += d[n] * (deg - 2)
                if weighted_cost < min_k_d_weight:
                    min_k_d_weight = weighted_cost
                    min_k_d = arborescence

            # 3. If sum of d_i * v_{i, k} is greater than zero, terminate
            if min_k_d_weight > 0:
                return d, min_k_d
            # 4. d_i = d_i + v_{i, k}
            for n, deg in min_k_d.degree:
                d[n] += deg - 2
            # Check that we do not need to terminate because the direction
            # of ascent does not exist. This is done with linear
            # programming.
            c = np.full(len(minimum_1_arborescences), -1, dtype=int)
            a_eq = np.empty((len(G) + 1, len(minimum_1_arborescences)), dtype=int)
            b_eq = np.zeros(len(G) + 1, dtype=int)
            b_eq[len(G)] = 1
            for arb_count, arborescence in enumerate(minimum_1_arborescences):
                n_count = len(G) - 1
                for n, deg in arborescence.degree:
                    a_eq[n_count][arb_count] = deg - 2
                    n_count -= 1
                a_eq[len(G)][arb_count] = 1
            program_result = sp.optimize.linprog(
                c, A_eq=a_eq, b_eq=b_eq, method="highs-ipm"
            )
            # If the constants exist, then the direction of ascent doesn't
            if program_result.success:
                # There is no direction of ascent
                return None, minimum_1_arborescences

            # 5. GO TO 2

    def find_epsilon(k, d):
        """
        Given the direction of ascent at pi, find the maximum distance we can go
        in that direction.

        Parameters
        ----------
        k_xy : set
            The set of 1-arborescences which have the minimum rate of increase
            in the direction of ascent

        d : dict
            The direction of ascent

        Returns
        -------
        float
            The distance we can travel in direction `d`
        """
        min_epsilon = math.inf
        for e_u, e_v, e_w in G.edges(data=weight):
            if (e_u, e_v) in k.edges:
                continue
            # Now, I have found a condition which MUST be true for the edges to
            # be a valid substitute. The edge in the graph which is the
            # substitute is the one with the same terminated end. This can be
            # checked rather simply.
            #
            # Find the edge within k which is the substitute. Because k is a
            # 1-arborescence, we know that they is only one such edges
            # leading into every vertex.
            if len(k.in_edges(e_v, data=weight)) > 1:
                raise Exception
            sub_u, sub_v, sub_w = next(k.in_edges(e_v, data=weight).__iter__())
            k.add_edge(e_u, e_v, **{weight: e_w})
            k.remove_edge(sub_u, sub_v)
            if (
                max(d for n, d in k.in_degree()) <= 1
                and len(G) == k.number_of_edges()
                and nx.is_weakly_connected(k)
            ):
                # Ascent method calculation
                if d[sub_u] == d[e_u] or sub_w == e_w:
                    # Revert to the original graph
                    k.remove_edge(e_u, e_v)
                    k.add_edge(sub_u, sub_v, **{weight: sub_w})
                    continue
                epsilon = (sub_w - e_w) / (d[e_u] - d[sub_u])
                if 0 < epsilon < min_epsilon:
                    min_epsilon = epsilon
            # Revert to the original graph
            k.remove_edge(e_u, e_v)
            k.add_edge(sub_u, sub_v, **{weight: sub_w})

        return min_epsilon

    # I have to know that the elements in pi correspond to the correct elements
    # in the direction of ascent, even if the node labels are not integers.
    # Thus, I will use dictionaries to made that mapping.
    pi_dict = {}
    for n in G:
        pi_dict[n] = 0
    del n
    original_edge_weights = {}
    for u, v, d in G.edges(data=True):
        original_edge_weights[(u, v)] = d[weight]
    dir_ascent, k_d = direction_of_ascent()
    while dir_ascent is not None:
        max_distance = find_epsilon(k_d, dir_ascent)
        for n, v in dir_ascent.items():
            pi_dict[n] += max_distance * v
        for u, v, d in G.edges(data=True):
            d[weight] = original_edge_weights[(u, v)] + pi_dict[u]
        dir_ascent, k_d = direction_of_ascent()
    nx._clear_cache(G)
    # k_d is no longer an individual 1-arborescence but rather a set of
    # minimal 1-arborescences at the maximum point of the polytope and should
    # be reflected as such
    k_max = k_d

    # Search for a cycle within k_max. If a cycle exists, return it as the
    # solution
    for k in k_max:
        if len([n for n in k if k.degree(n) == 2]) == G.order():
            # Tour found
            # TODO: this branch does not restore original_edge_weights of G!
            return k.size(weight), k

    # Write the original edge weights back to G and every member of k_max at
    # the maximum point. Also average the number of times that edge appears in
    # the set of minimal 1-arborescences.
    x_star = {}
    size_k_max = len(k_max)
    for u, v, d in G.edges(data=True):
        edge_count = 0
        d[weight] = original_edge_weights[(u, v)]
        for k in k_max:
            if (u, v) in k.edges():
                edge_count += 1
                k[u][v][weight] = original_edge_weights[(u, v)]
        x_star[(u, v)] = edge_count / size_k_max
    # Now symmetrize the edges in x_star and scale them according to (5) in
    # reference [1]
    z_star = {}
    scale_factor = (G.order() - 1) / G.order()
    for u, v in x_star:
        frequency = x_star[(u, v)] + x_star[(v, u)]
        if frequency > 0:
            z_star[(u, v)] = scale_factor * frequency
    del x_star
    # Return the optimal weight and the z dict
    return next(k_max.__iter__()).size(weight), z_star

