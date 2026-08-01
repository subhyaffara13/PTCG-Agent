
def _get_external_inputs(
    region: Region,
) -> dict[Node, OrderedSet[UsageIndex]]:
    external_node_to_usages = defaultdict[Node, OrderedSet[UsageIndex]](OrderedSet)
    region_unique = set(region)
    for node_ind, node in enumerate(region):
        flattened_args_kwargs = _get_flat_args(node, {})
        for arg_ind, in_node in enumerate(flattened_args_kwargs):
            if isinstance(in_node, Node) and in_node not in region_unique:
                # in_node may occur in multiple nodes' flat_args
                # track this so we can check if the arg is mutated
                # Previously, we only needed to track one occurrence
                # to be able to map that node to a placeholder
                external_node_to_usages[in_node].add((node_ind, arg_ind))

    return external_node_to_usages

