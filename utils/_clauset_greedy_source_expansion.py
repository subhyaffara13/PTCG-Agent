
def _clauset_greedy_source_expansion(G, *, source, cutoff=None):
    if cutoff is None:
        cutoff = float("inf")
    C = {source}
    B = {source}
    U = G[source].keys() - C
    T = {frozenset([node, nbr]) for node in B for nbr in G.neighbors(node)}
    I = {edge for edge in T if all(node in C for node in edge)}

    R_value = 0
    while len(C) < cutoff:
        if not U:
            break

        max_R = 0
        best_node = None
        best_node_B = best_node_T = best_node_I = set()

        for v in U:
            R_tmp, B_tmp, T_tmp, I_tmp = _calculate_local_modularity_for_candidate(
                G, v, C, B, T, I
            )
            if R_tmp > max_R:
                max_R = R_tmp
                best_node = v
                best_node_B = B_tmp
                best_node_T = T_tmp
                best_node_I = I_tmp

        C = C | {best_node}
        U.update(G[best_node].keys() - C)
        U.remove(best_node)
        B = best_node_B
        T = best_node_T
        I = best_node_I
        if max_R < R_value:
            break
        R_value = max_R

    return C

