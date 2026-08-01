
def _restore_Tinout_Di(popped_node1, popped_node2, graph_params, state_params):
    # If the node we want to remove from the mapping, has at least one covered neighbor, add it to T1.
    G1, G2, _, _, _, _, _ = graph_params
    (
        mapping,
        reverse_mapping,
        T1,
        T1_in,
        T1_tilde,
        T1_tilde_in,
        T2,
        T2_in,
        T2_tilde,
        T2_tilde_in,
    ) = state_params

    is_added = False
    for successor in G1[popped_node1]:
        if successor in mapping:
            # if a neighbor of the excluded node1 is in the mapping, keep node1 in T1
            is_added = True
            T1_in.add(popped_node1)
        else:
            # check if its neighbor has another connection with a covered node.
            # If not, only then exclude it from T1
            if not any(pred in mapping for pred in G1.pred[successor]):
                T1.discard(successor)

            if not any(succ in mapping for succ in G1[successor]):
                T1_in.discard(successor)

            if successor not in T1:
                if successor not in T1_in:
                    T1_tilde.add(successor)

    for predecessor in G1.pred[popped_node1]:
        if predecessor in mapping:
            # if a neighbor of the excluded node1 is in the mapping, keep node1 in T1
            is_added = True
            T1.add(popped_node1)
        else:
            # check if its neighbor has another connection with a covered node.
            # If not, only then exclude it from T1
            if not any(pred in mapping for pred in G1.pred[predecessor]):
                T1.discard(predecessor)

            if not any(succ in mapping for succ in G1[predecessor]):
                T1_in.discard(predecessor)

            if not (predecessor in T1 or predecessor in T1_in):
                T1_tilde.add(predecessor)

    # Case where the node is not present in neither the mapping nor T1.
    # By definition it should belong to T1_tilde
    if not is_added:
        T1_tilde.add(popped_node1)

    is_added = False
    for successor in G2[popped_node2]:
        if successor in reverse_mapping:
            is_added = True
            T2_in.add(popped_node2)
        else:
            if not any(pred in reverse_mapping for pred in G2.pred[successor]):
                T2.discard(successor)

            if not any(succ in reverse_mapping for succ in G2[successor]):
                T2_in.discard(successor)

            if successor not in T2:
                if successor not in T2_in:
                    T2_tilde.add(successor)

    for predecessor in G2.pred[popped_node2]:
        if predecessor in reverse_mapping:
            # if a neighbor of the excluded node1 is in the mapping, keep node1 in T1
            is_added = True
            T2.add(popped_node2)
        else:
            # check if its neighbor has another connection with a covered node.
            # If not, only then exclude it from T1
            if not any(pred in reverse_mapping for pred in G2.pred[predecessor]):
                T2.discard(predecessor)

            if not any(succ in reverse_mapping for succ in G2[predecessor]):
                T2_in.discard(predecessor)

            if not (predecessor in T2 or predecessor in T2_in):
                T2_tilde.add(predecessor)

    if not is_added:
        T2_tilde.add(popped_node2)

