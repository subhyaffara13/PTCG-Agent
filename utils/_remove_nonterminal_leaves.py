
def _remove_nonterminal_leaves(G, terminals):
    terminal_set = set(terminals)
    leaves = {n for n in G if len(set(G[n]) - {n}) == 1}
    nonterminal_leaves = leaves - terminal_set

    while nonterminal_leaves:
        # Removing a node may create new non-terminal leaves, so we limit
        # search for candidate non-terminal nodes to neighbors of current
        # non-terminal nodes
        candidate_leaves = set.union(*(set(G[n]) for n in nonterminal_leaves))
        candidate_leaves -= nonterminal_leaves | terminal_set
        # Remove current set of non-terminal nodes
        G.remove_nodes_from(nonterminal_leaves)
        # Find any new non-terminal nodes from the set of candidates
        leaves = {n for n in candidate_leaves if len(set(G[n]) - {n}) == 1}
        nonterminal_leaves = leaves - terminal_set

