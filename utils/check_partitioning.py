
def check_partitioning(
    main_graph: onnx.GraphProto,
    supported_ops_checker: _SupportedOpsChecker,
    require_fixed_input_sizes: bool,
    max_rank: int = 999,
) -> PartitioningInfo:
    """
    Estimate the partitions the graph will be split into for nodes that is_node_supported_fn returns true for.

    The check on whether a node is supported is purely based on the operator type. Additional limitations
    (e.g. NNAPI EP only supports 2D Conv) are not checked, so partitions may not be 100% accurate. The limitations
    for operators in the partitions are printed so the user can manually check.
    :param main_graph: Graph to process
    :param supported_ops_checker: Checker with info on supported ops.
    :param require_fixed_input_sizes: If True, require that the inputs to a potentially supported node are fixed size
                                      tensors for it to be considered as supported. This requires
                                      onnx.shape_inference.infer_shapes to have been run on the model to populate the
                                      shape information.
                                      If False, shapes are ignored during the check.
    :param max_rank: Set if EP has a limitation on the rank of tensors it supports.
    :return PartitioningInfo instance with details
    """

    if require_fixed_input_sizes and len(main_graph.value_info) == 0 and len(main_graph.node) > 1:
        raise ValueError("Run onnx.shape_inference.infer_shapes on the model to populate the shape information.")

    # create lookup map from ValueInfo for efficiency
    def _update_value_info(graph: onnx.GraphProto, value_to_shape: dict[str, onnx.ValueInfoProto]):
        for v in graph.input:
            value_to_shape[v.name] = v
        for v in graph.output:
            value_to_shape[v.name] = v
        for v in graph.value_info:
            value_to_shape[v.name] = v

    # the producer/consumer maps are for the entire model
    node_to_producers, node_to_consumers = get_producer_consumer_maps(main_graph)

    def _check_graph(
        graph: onnx.GraphProto,
        outer_scope_value_info: dict[str, onnx.ValueInfoProto] | None,
        outer_scope_initializers: set[str] | None = None,
        partitioning_info: PartitioningInfo | None = None,
    ) -> PartitioningInfo:
        if outer_scope_value_info is not None:
            # extend value info if we're using it. we replace any value shadowed with a local one
            value_info = outer_scope_value_info.copy()
            _update_value_info(graph, value_info)
        else:
            value_info = {}

        if outer_scope_initializers is None:
            outer_scope_initializers = set()

        info = _check_partitioning_for_graph(
            graph,
            node_to_producers,
            node_to_consumers,
            supported_ops_checker,
            outer_scope_initializers,
            require_fixed_input_sizes,
            value_info,
            max_rank,
        )

        if partitioning_info:
            # merge in subgraph info
            partitioning_info.merge(info)
        else:
            # main graph info
            partitioning_info = info

        # setup outer scope initializers. we copy the input set as a model may have multiple subgraphs
        # on multiple levels, so we need to keep the set for each descent separate
        subgraph_outer_scope_initializers = set(outer_scope_initializers)
        for initializer in graph.initializer:
            subgraph_outer_scope_initializers.add(initializer.name)

        for node in graph.node:
            # recurse into nodes with subgraphs
            for attr in node.attribute:
                if attr.HasField("g"):
                    subgraph = attr.g
                    partitioning_info = _check_graph(
                        subgraph, value_info, subgraph_outer_scope_initializers, partitioning_info
                    )

        return partitioning_info

    aggregated_partitioning_info = _check_graph(main_graph, {} if require_fixed_input_sizes else None)

    return aggregated_partitioning_info

