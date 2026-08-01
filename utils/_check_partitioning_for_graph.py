
def _check_partitioning_for_graph(
    graph: onnx.GraphProto,
    node_to_producers: dict[onnx.NodeProto, set[onnx.NodeProto]],
    node_to_consumers: dict[onnx.NodeProto, set[onnx.NodeProto]],
    supported_ops_checker: _SupportedOpsChecker,
    outer_scope_initializers: set[str],
    require_fixed_input_sizes: bool,
    value_info: dict[str, onnx.ValueInfoProto],
    max_rank: int = 999,  # max rank if EP has a limitation
):
    # initializers have fixed sizes.
    initializers = [i.name for i in graph.initializer]

    def _is_fixed_shape_value(value):
        if value in value_info:
            return is_fixed_size_tensor(value_info[value])

        if value in initializers or value in outer_scope_initializers:
            return True

        # if something has an unknown shape (e.g. something downstream of a Reshape with dynamic input for the shape)
        # it won't have an entry in value_info
        return False

    #
    # Replicate logic from /onnxruntime/core/providers/partitioning_utils.cc:CreateSupportedPartitionNodeGroups
    # to roughly estimate number of partitions for nodes that is_node_supported_fn returns true for.
    #
    # We keep the structure and variable names as close as possible to the C++ implementation to simplify keeping them
    # in sync if future updates are needed.
    #
    # NOTE: CreateSupportedPartitionNodeGroups was recently updated to be QDQ aware so that partitions did not split
    # QDQ node groups. This code does not need to be QDQ aware as splitting a QDQ node group does not affect the total
    # number of partitions or supported nodes.
    #

    # we don't currently support a callback for additional group closure checks in the python implementation
    on_group_closed_fn = None

    supported_groups = []
    # number of inputs from unprocessed nodes (in-degree) per node
    in_degree = {}
    # nodes that are ready to process
    nodes_to_process = deque()  # deque of Node instances
    # nodes that will be processed when considering the next partition node group
    nodes_to_process_with_next_group = deque()

    # initialize in-degrees and find root nodes
    for node in graph.node:
        node_input_edge_count = len(node_to_producers[node]) if node in node_to_producers else 0
        in_degree[node] = node_input_edge_count
        if node_input_edge_count == 0:
            # node is only dependent on graph input or initializers
            nodes_to_process.append(node)

    supported_group = []
    # the partition node group's border is the aggregate of its nodes' output nodes
    supported_group_border = set()
    num_supported_nodes = 0
    num_unsupported_nodes_due_to_op = 0
    num_unsupported_nodes_due_to_dynamic_input = 0
    num_unsupported_nodes_due_to_rank = 0
    unsupported_ops = set()
    ops_with_unsupported_rank = set()

    def close_group():
        if supported_group:
            keep_partition = not on_group_closed_fn or on_group_closed_fn(supported_group)

            if keep_partition:
                supported_groups.append(supported_group.copy())

            supported_group.clear()
            supported_group_border.clear()

    while nodes_to_process or nodes_to_process_with_next_group:
        if not nodes_to_process:
            close_group()
            nodes_to_process = nodes_to_process_with_next_group
            nodes_to_process_with_next_group = deque()
            continue

        node = nodes_to_process.popleft()

        is_op_supported = supported_ops_checker.is_op_supported(node)
        is_input_shape_supported = not require_fixed_input_sizes or all(_is_fixed_shape_value(i) for i in node.input)

        is_rank_supported = True
        if value_info:
            for node_input in node.input:
                if node_input and node_input in value_info and value_info[node_input].type.HasField("tensor_type"):
                    input_rank = len(value_info[node_input].type.tensor_type.shape.dim)
                    if input_rank > max_rank:
                        is_rank_supported = False
                        break

        # special-case if we can infer the rank from the length of the 'perms' Transpose attribute
        # e.g. this works with SegmentAnything where dynamic Reshape operators result in no shape info.
        if node.op_type == "Transpose" and len(node.attribute[0].ints) > max_rank:
            is_rank_supported = False

        is_node_supported = is_op_supported and is_input_shape_supported and is_rank_supported

        if not is_node_supported:
            if node in supported_group_border:
                # an unsupported node on the border will be processed after the current partition node group
                # so skip any additional processing/counting here
                nodes_to_process_with_next_group.append(node)
                continue

            if not is_op_supported:
                unsupported_ops.add(f"{node.domain if node.domain else 'ai.onnx'}:{node.op_type}")
                num_unsupported_nodes_due_to_op += 1

            if not is_input_shape_supported:
                num_unsupported_nodes_due_to_dynamic_input += 1

            if not is_rank_supported:
                num_unsupported_nodes_due_to_rank += 1
                ops_with_unsupported_rank.add(f"{node.domain if node.domain else 'ai.onnx'}:{node.op_type}")

        if is_node_supported:
            num_supported_nodes += 1

            # add node to the partition node group
            supported_group.append(node)

            # remove node from the border and add its outputs to the border
            if node in supported_group_border:  # noqa: FURB132
                supported_group_border.remove(node)

            # for each consumer node add to supported_group_border
            if node in node_to_consumers:
                for consumer in node_to_consumers[node]:
                    supported_group_border.add(consumer)

        # adjust in-degrees of the node outputs and add any new nodes to process
        if node in node_to_consumers:
            for consumer in node_to_consumers[node]:
                consumer_node_in_degree = in_degree[consumer]
                consumer_node_in_degree -= 1
                if consumer_node_in_degree == 0:
                    nodes_to_process.append(consumer)

                in_degree[consumer] = consumer_node_in_degree

    close_group()

    num_nodes = len(graph.node)
    num_partitions = len(supported_groups)

    info = PartitioningInfo(
        num_nodes,
        num_supported_nodes,
        num_partitions,
        supported_ops_checker,
        supported_groups,
        unsupported_ops,
        num_unsupported_nodes_due_to_op,
        num_unsupported_nodes_due_to_dynamic_input,
        num_unsupported_nodes_due_to_rank,
        ops_with_unsupported_rank,
    )

    return info

