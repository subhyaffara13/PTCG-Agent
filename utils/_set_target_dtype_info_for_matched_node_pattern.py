
def _set_target_dtype_info_for_matched_node_pattern(
    matched_node_pattern: NodePattern,
    last_node: Node,
    qconfig: QConfigAny,
    qhandler: QuantizeHandler | None,
    backend_config: BackendConfig,
    named_modules: dict[str, torch.nn.Module],
    cache_for_no_tensor_check: dict[Node, bool],
    processed_nodes: set[Node],
) -> None:
    """Sets the target_dtype_info for each node in matched_node_pattern
    Note: processed_nodes is used to ensure we only process each node once
    """
    if isinstance(matched_node_pattern, (list, tuple)):  # noqa: UP038
        for node_pattern in matched_node_pattern:
            _set_target_dtype_info_for_matched_node_pattern(
                node_pattern,
                last_node,
                qconfig,
                qhandler,
                backend_config,
                named_modules,
                cache_for_no_tensor_check,
                processed_nodes,
            )

    # set target_dtype_info if matched_node_pattern is a Node
    # other types of matched object, e.g. int, float literals, are ignored
    elif isinstance(matched_node_pattern, Node):
        # for pyre
        if not isinstance(matched_node_pattern, Node):
            raise AssertionError("matched_node_pattern must be a Node")
        node = matched_node_pattern
        if node in processed_nodes:
            return
        processed_nodes.add(node)

        if qconfig is None:
            return
        # TODO: refactor the following code in terms of apply a qconfig to a pattern
        # e.g. for a pattern with op1 -> op2 -> op3, and qconfig = QConfig(input_act=obs0, output_act=obs1)
        # we set the input_obs_or_fq_ctr for the arguments of op1 to based on qconfig.input_act,
        # and set output_obs_or_fq_ctr based on qconfig.output_act
        # this also requires we extend the structure of QConfig to support more fine
        # grained configurations
        target_dtype_info: dict[str, Any] = _get_target_activation_dtype_for_node(
            node,
            qconfig,
            qhandler,
            named_modules,
            backend_config,
            cache_for_no_tensor_check,
        )
        node.meta["target_dtype_info"] = target_dtype_info

