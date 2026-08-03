import random

def test_tree_isomorphic_all_non_isomorphic_trees_relabeled(n):
    """Tests every non-isomorphic tree with `n` nodes is isomorphic with a
    copy of itself with an arbitrary node-remapping."""
    for tree in nx.nonisomorphic_trees(n):
        nodes = list(tree)
        random.shuffle(shuffled := nodes.copy())
        node_mapping = dict(zip(nodes, shuffled))
        # Shuffle the edge list to ensure no dependence on edge order
        random.shuffle(
            new_edges := [
                # Randomly order edges to ensure no dependence on node order within edges
                (node_mapping[u], node_mapping[v])
                if random.randint(0, 1)
                else (node_mapping[v], node_mapping[u])
                for (u, v) in tree.edges
            ]
        )
        relabeled = nx.Graph(new_edges)
        # Does not necessarily have to be the same as node_mapping
        iso_mapping = nx.isomorphism.tree_isomorphism(tree, relabeled)

        assert iso_mapping != []
        assert _check_isomorphism(tree, relabeled, iso_mapping)

