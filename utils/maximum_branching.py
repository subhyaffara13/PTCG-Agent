
def maximum_branching(
    G,
    attr="weight",
    default=1,
    preserve_attrs=False,
    partition=None,
):
    #######################################
    ### Data Structure Helper Functions ###
    #######################################

    def edmonds_add_edge(G, edge_index, u, v, key, **d):
        """
        Adds an edge to `G` while also updating the edge index.

        This algorithm requires the use of an external dictionary to track
        the edge keys since it is possible that the source or destination
        node of an edge will be changed and the default key-handling
        capabilities of the MultiDiGraph class do not account for this.

        Parameters
        ----------
        G : MultiDiGraph
            The graph to insert an edge into.
        edge_index : dict
            A mapping from integers to the edges of the graph.
        u : node
            The source node of the new edge.
        v : node
            The destination node of the new edge.
        key : int
            The key to use from `edge_index`.
        d : keyword arguments, optional
            Other attributes to store on the new edge.
        """

        if key in edge_index:
            uu, vv, _ = edge_index[key]
            if (u != uu) or (v != vv):
                raise Exception(f"Key {key!r} is already in use.")

        G.add_edge(u, v, key, **d)
        edge_index[key] = (u, v, G.succ[u][v][key])

    def edmonds_remove_node(G, edge_index, n):
        """
        Remove a node from the graph, updating the edge index to match.

        Parameters
        ----------
        G : MultiDiGraph
            The graph to remove an edge from.
        edge_index : dict
            A mapping from integers to the edges of the graph.
        n : node
            The node to remove from `G`.
        """
        keys = set()
        for keydict in G.pred[n].values():
            keys.update(keydict)
        for keydict in G.succ[n].values():
            keys.update(keydict)

        for key in keys:
            del edge_index[key]

        G.remove_node(n)

    #######################
    ### Algorithm Setup ###
    #######################

    # Pick an attribute name that the original graph is unlikly to have
    candidate_attr = "edmonds' secret candidate attribute"
    new_node_base_name = "edmonds new node base name "

    G_original = G
    G = nx.MultiDiGraph()
    G.__networkx_cache__ = None  # Disable caching

    # A dict to reliably track mutations to the edges using the key of the edge.
    G_edge_index = {}
    # Each edge is given an arbitrary numerical key
    for key, (u, v, data) in enumerate(G_original.edges(data=True)):
        d = {attr: data.get(attr, default)}

        if data.get(partition) is not None:
            d[partition] = data.get(partition)

        if preserve_attrs:
            for d_k, d_v in data.items():
                if d_k != attr:
                    d[d_k] = d_v

        edmonds_add_edge(G, G_edge_index, u, v, key, **d)

    level = 0  # Stores the number of contracted nodes

    # These are the buckets from the paper.
    #
    # In the paper, G^i are modified versions of the original graph.
    # D^i and E^i are the nodes and edges of the maximal edges that are
    # consistent with G^i. In this implementation, D^i and E^i are stored
    # together as the graph B^i. We will have strictly more B^i then the
    # paper will have.
    #
    # Note that the data in graphs and branchings are tuples with the graph as
    # the first element and the edge index as the second.
    B = nx.MultiDiGraph()
    B_edge_index = {}
    graphs = []  # G^i list
    branchings = []  # B^i list
    selected_nodes = set()  # D^i bucket
    uf = nx.utils.UnionFind()

    # A list of lists of edge indices. Each list is a circuit for graph G^i.
    # Note the edge list is not required to be a circuit in G^0.
    circuits = []

    # Stores the index of the minimum edge in the circuit found in G^i and B^i.
    # The ordering of the edges seems to preserver the weight ordering from
    # G^0. So even if the circuit does not form a circuit in G^0, it is still
    # true that the minimum edges in circuit G^0 (despite their weights being
    # different)
    minedge_circuit = []

    ###########################
    ### Algorithm Structure ###
    ###########################

    # Each step listed in the algorithm is an inner function. Thus, the overall
    # loop structure is:
    #
    # while True:
    #     step_I1()
    #     if cycle detected:
    #         step_I2()
    #     elif every node of G is in D and E is a branching:
    #         break

    ##################################
    ### Algorithm Helper Functions ###
    ##################################

    def edmonds_find_desired_edge(v):
        """
        Find the edge directed towards v with maximal weight.

        If an edge partition exists in this graph, return the included
        edge if it exists and never return any excluded edge.

        Note: There can only be one included edge for each vertex otherwise
        the edge partition is empty.

        Parameters
        ----------
        v : node
            The node to search for the maximal weight incoming edge.
        """
        edge = None
        max_weight = -INF
        for u, _, key, data in G.in_edges(v, data=True, keys=True):
            # Skip excluded edges
            if data.get(partition) == nx.EdgePartition.EXCLUDED:
                continue

            new_weight = data[attr]

            # Return the included edge
            if data.get(partition) == nx.EdgePartition.INCLUDED:
                max_weight = new_weight
                edge = (u, v, key, new_weight, data)
                break

            # Find the best open edge
            if new_weight > max_weight:
                max_weight = new_weight
                edge = (u, v, key, new_weight, data)

        return edge, max_weight

    def edmonds_step_I2(v, desired_edge, level):
        """
        Perform step I2 from Edmonds' paper

        First, check if the last step I1 created a cycle. If it did not, do nothing.
        If it did, store the cycle for later reference and contract it.

        Parameters
        ----------
        v : node
            The current node to consider
        desired_edge : edge
            The minimum desired edge to remove from the cycle.
        level : int
            The current level, i.e. the number of cycles that have already been removed.
        """
        u = desired_edge[0]

        Q_nodes = nx.shortest_path(B, v, u)
        Q_edges = [
            list(B[Q_nodes[i]][vv].keys())[0] for i, vv in enumerate(Q_nodes[1:])
        ]
        Q_edges.append(desired_edge[2])  # Add the new edge key to complete the circuit

        # Get the edge in the circuit with the minimum weight.
        # Also, save the incoming weights for each node.
        minweight = INF
        minedge = None
        Q_incoming_weight = {}
        for edge_key in Q_edges:
            u, v, data = B_edge_index[edge_key]
            w = data[attr]
            # We cannot remove an included edge, even if it is the
            # minimum edge in the circuit
            Q_incoming_weight[v] = w
            if data.get(partition) == nx.EdgePartition.INCLUDED:
                continue
            if w < minweight:
                minweight = w
                minedge = edge_key

        circuits.append(Q_edges)
        minedge_circuit.append(minedge)
        graphs.append((G.copy(), G_edge_index.copy()))
        branchings.append((B.copy(), B_edge_index.copy()))

        # Mutate the graph to contract the circuit
        new_node = new_node_base_name + str(level)
        G.add_node(new_node)
        new_edges = []
        for u, v, key, data in G.edges(data=True, keys=True):
            if u in Q_incoming_weight:
                if v in Q_incoming_weight:
                    # Circuit edge. For the moment do nothing,
                    # eventually it will be removed.
                    continue
                else:
                    # Outgoing edge from a node in the circuit.
                    # Make it come from the new node instead
                    dd = data.copy()
                    new_edges.append((new_node, v, key, dd))
            else:
                if v in Q_incoming_weight:
                    # Incoming edge to the circuit.
                    # Update it's weight
                    w = data[attr]
                    w += minweight - Q_incoming_weight[v]
                    dd = data.copy()
                    dd[attr] = w
                    new_edges.append((u, new_node, key, dd))
                else:
                    # Outside edge. No modification needed
                    continue

        for node in Q_nodes:
            edmonds_remove_node(G, G_edge_index, node)
            edmonds_remove_node(B, B_edge_index, node)

        selected_nodes.difference_update(set(Q_nodes))

        for u, v, key, data in new_edges:
            edmonds_add_edge(G, G_edge_index, u, v, key, **data)
            if candidate_attr in data:
                del data[candidate_attr]
                edmonds_add_edge(B, B_edge_index, u, v, key, **data)
                uf.union(u, v)

    def is_root(G, u, edgekeys):
        """
        Returns True if `u` is a root node in G.

        Node `u` is a root node if its in-degree over the specified edges is zero.

        Parameters
        ----------
        G : Graph
            The current graph.
        u : node
            The node in `G` to check if it is a root.
        edgekeys : iterable of edges
            The edges for which to check if `u` is a root of.
        """
        if u not in G:
            raise Exception(f"{u!r} not in G")

        for v in G.pred[u]:
            for edgekey in G.pred[u][v]:
                if edgekey in edgekeys:
                    return False, edgekey
        else:
            return True, None

    nodes = iter(list(G.nodes))
    while True:
        try:
            v = next(nodes)
        except StopIteration:
            # If there are no more new nodes to consider, then we should
            # meet stopping condition (b) from the paper:
            #   (b) every node of G^i is in D^i and E^i is a branching
            assert len(G) == len(B)
            if len(B):
                assert is_branching(B)

            graphs.append((G.copy(), G_edge_index.copy()))
            branchings.append((B.copy(), B_edge_index.copy()))
            circuits.append([])
            minedge_circuit.append(None)

            break
        else:
            #####################
            ### BEGIN STEP I1 ###
            #####################

            # This is a very simple step, so I don't think it needs a method of it's own
            if v in selected_nodes:
                continue

        selected_nodes.add(v)
        B.add_node(v)
        desired_edge, desired_edge_weight = edmonds_find_desired_edge(v)

        # There might be no desired edge if all edges are excluded or
        # v is the last node to be added to B, the ultimate root of the branching
        if desired_edge is not None and desired_edge_weight > 0:
            u = desired_edge[0]
            # Flag adding the edge will create a circuit before merging the two
            # connected components of u and v in B
            circuit = uf[u] == uf[v]
            dd = {attr: desired_edge_weight}
            if desired_edge[4].get(partition) is not None:
                dd[partition] = desired_edge[4].get(partition)

            edmonds_add_edge(B, B_edge_index, u, v, desired_edge[2], **dd)
            G[u][v][desired_edge[2]][candidate_attr] = True
            uf.union(u, v)

            ###################
            ### END STEP I1 ###
            ###################

            #####################
            ### BEGIN STEP I2 ###
            #####################

            if circuit:
                edmonds_step_I2(v, desired_edge, level)
                nodes = iter(list(G.nodes()))
                level += 1

            ###################
            ### END STEP I2 ###
            ###################

    #####################
    ### BEGIN STEP I3 ###
    #####################

    # Create a new graph of the same class as the input graph
    H = G_original.__class__()

    # Start with the branching edges in the last level.
    edges = set(branchings[level][1])
    while level > 0:
        level -= 1

        # The current level is i, and we start counting from 0.
        #
        # We need the node at level i+1 that results from merging a circuit
        # at level i. basename_0 is the first merged node and this happens
        # at level 1. That is basename_0 is a node at level 1 that results
        # from merging a circuit at level 0.

        merged_node = new_node_base_name + str(level)
        circuit = circuits[level]
        isroot, edgekey = is_root(graphs[level + 1][0], merged_node, edges)
        edges.update(circuit)

        if isroot:
            minedge = minedge_circuit[level]
            if minedge is None:
                raise Exception

            # Remove the edge in the cycle with minimum weight
            edges.remove(minedge)
        else:
            # We have identified an edge at the next higher level that
            # transitions into the merged node at this level. That edge
            # transitions to some corresponding node at the current level.
            #
            # We want to remove an edge from the cycle that transitions
            # into the corresponding node, otherwise the result would not
            # be a branching.

            G, G_edge_index = graphs[level]
            target = G_edge_index[edgekey][1]
            for edgekey in circuit:
                u, v, data = G_edge_index[edgekey]
                if v == target:
                    break
            else:
                raise Exception("Couldn't find edge incoming to merged node.")

            edges.remove(edgekey)

    H.add_nodes_from(G_original)
    for edgekey in edges:
        u, v, d = graphs[0][1][edgekey]
        dd = {attr: d[attr]}

        if preserve_attrs:
            for key, value in d.items():
                if key not in [attr, candidate_attr]:
                    dd[key] = value

        H.add_edge(u, v, **dd)

    ###################
    ### END STEP I3 ###
    ###################

    return H

