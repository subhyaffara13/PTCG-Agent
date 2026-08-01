
def _add_loggers_impl(
    name_a: str,
    gm_a: GraphModule,
    name_b: str,
    gm_b: GraphModule,
    logger_cls: Callable,
    should_log_inputs: bool,
    base_name_to_sets_of_related_ops: dict[str, set[NSNodeTargetType]] | None = None,
    unmatchable_types_map: dict[str, set[NSNodeTargetType]] | None = None,
) -> tuple[nn.Module, nn.Module]:
    torch._C._log_api_usage_once("quantization_api._numeric_suite_fx._add_loggers_impl")
    matched_subgraph_pairs = get_matching_subgraph_pairs(
        gm_a, gm_b, base_name_to_sets_of_related_ops, unmatchable_types_map
    )
    nodes_and_names_to_instrument_inputs_a = []
    nodes_and_names_to_instrument_inputs_b = []
    nodes_and_names_to_instrument_outputs_a = []
    nodes_and_names_to_instrument_outputs_b = []
    for match_name, (subgraph_a, subgraph_b) in matched_subgraph_pairs.items():
        ref_node_type_a = get_target_type_str(subgraph_a.base_op_node, gm_a)
        ref_node_type_b = get_target_type_str(subgraph_b.base_op_node, gm_b)
        # Note: for matching inputs we use start_node, such as observing
        # the input of linear in linear-relu
        if should_log_inputs:
            nodes_and_names_to_instrument_inputs_a.append(
                (subgraph_a.start_node, match_name, ref_node_type_a)
            )
            nodes_and_names_to_instrument_inputs_b.append(
                (subgraph_b.start_node, match_name, ref_node_type_b)
            )
        # Note: for matching activations we always use end_node,
        # such as observing the output of relu in linear-relu
        nodes_and_names_to_instrument_outputs_a.append(
            (subgraph_a.end_node, match_name, ref_node_type_a)
        )
        nodes_and_names_to_instrument_outputs_b.append(
            (subgraph_b.end_node, match_name, ref_node_type_b)
        )

    new_model_a = _add_loggers_one_model(
        name_a,
        gm_a,
        nodes_and_names_to_instrument_inputs_a,
        nodes_and_names_to_instrument_outputs_a,
        logger_cls,
    )
    new_model_b = _add_loggers_one_model(
        name_b,
        gm_b,
        nodes_and_names_to_instrument_inputs_b,
        nodes_and_names_to_instrument_outputs_b,
        logger_cls,
    )
    return (new_model_a, new_model_b)

