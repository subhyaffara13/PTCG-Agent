
def apply_graph_deduplication(output_graph) -> dict[str, torch.fx.GraphModule]:  # type: ignore[no-untyped-def]
    """
    This is the main entry point for applying the graph deduplication pass. \
Deduplication occurs in two phases:
    1. Subgraph creation:
        Subgraph creation works by taking one representative region from each region \
group and creating a subgraph from it, which will then be used to replace all regions \
in the group. This is implemented by first copying all nodes of the region to the new \
subgraph and then finding all inputs which are not within the region and creating placeholders \
for them. For the outputs, all regions in a region group need to be scanned to ensure the \
largest set of outputs is found, and then an output node is created which returns \
a tuple of all outputs.

    2. Graph replacement:
        To replace each region with the extracted subgraph, the node index in the region \
and argument index within the node's flattened args and kwargs are recorded once during \
subgraph creation. This allows us to determine which (external to the region) nodes and \
in which order these nodes are passed as inputs. For the outputs, getitem nodes are created \
for each output, and all nodes in the region with external outputs are replaced by the proper \
getitem node. Finally, all original nodes are erased (there should be no uses of these \
left in the graph).

The deduplication mutates the output_graph argument in place.

Returns a mapping of nodes to their subgraph output replacement node to remap outputs
when they are created in output_graph.
    """

    duplicated_region_groups = output_graph.region_tracker.get_identical_regions(
        output_graph.graph
    )
    node_to_mutated_arg_positions = (
        output_graph.region_tracker.node_to_mutated_arg_positions
    )
    node_to_additional_deps = _populate_additional_deps(
        output_graph.graph, output_graph.region_tracker.node_to_mutated_arg_positions
    )

    sub_gms: dict[str, torch.fx.GraphModule] = {}

    for region_group in duplicated_region_groups:
        inds_with_external_users = _get_all_output_indices(region_group)
        region = region_group[0]
        (
            subgraph,
            external_node_usages,
            node_usage_to_tuple_elems,
            ind_to_tuple_spec,
        ) = _create_subgraph(region, inds_with_external_users)

        # Ignore regions with no args for now, could they possibly be evaluated at compile time?
        if not list(external_node_usages):
            continue

        sub_gm = torch.fx.GraphModule(output_graph.nn_modules, subgraph)
        subgraph_name = output_graph.install_subgraph("subgraph", sub_gm)
        sub_gms[subgraph_name] = sub_gm
        with output_graph.graph.inserting_before():
            get_subgraph_node = output_graph.graph.create_node(
                "get_attr", subgraph_name, (), {}
            )

        for region in region_group:
            _replace_region_with_subgraph(
                output_graph.graph,
                region,
                get_subgraph_node,
                external_node_usages,
                node_usage_to_tuple_elems,
                ind_to_tuple_spec,
                inds_with_external_users,
                subgraph_name,
                node_to_additional_deps,
                node_to_mutated_arg_positions,
            )

    # This is to expose the updated node_to_additional_deps to tests
    global last_node_to_additional_deps
    last_node_to_additional_deps = node_to_additional_deps

    _stable_topological_sort(
        output_graph.graph,
        node_to_additional_deps,
    )
    return sub_gms

