
def _get_ordered_seq_nr_groups(
    gm: GraphModule | list[GraphModule],
) -> list[list[str]]:
    """
    Group call_function nodes by seq_nr, order by seq_nr value,
    and return a list of lists of node names (sorted alphabetically).

    Args:
        gm: A single GraphModule or a list of GraphModules to process.
            When a list is provided, nodes from all graphs are grouped together.

    Returns:
        A list of lists, where each inner list contains node names that share the same seq_nr,
        sorted alphabetically. The outer list is ordered by seq_nr value.
    """
    # Normalize input to a list
    if isinstance(gm, GraphModule):
        gms = [gm]
    else:
        gms = gm

    seq_nr_dict: dict[int, list[str]] = defaultdict(list)
    for graph_module in gms:
        for node in graph_module.graph.nodes:
            if node.op == "call_function":
                seq_nr = node.meta.get("seq_nr")
                if seq_nr is not None:
                    seq_nr_dict[seq_nr].append(node.name)
    # Sort by seq_nr and return list of sorted lists
    return [sorted(seq_nr_dict[k]) for k in sorted(seq_nr_dict.keys())]

