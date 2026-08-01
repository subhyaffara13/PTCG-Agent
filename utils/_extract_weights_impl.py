
def _extract_weights_impl(
    model_name_a: str,
    gm_a: GraphModule,
    model_name_b: str,
    gm_b: GraphModule,
    base_name_to_sets_of_related_ops: dict[str, set[NSNodeTargetType]] | None = None,
    unmatchable_types_map: dict[str, set[NSNodeTargetType]] | None = None,
    op_to_type_to_weight_extraction_fn: dict[str, dict[Callable, Callable]]
    | None = None,
) -> NSResultsType:
    torch._C._log_api_usage_once(
        "quantization_api._numeric_suite_fx._extract_weights_impl"
    )
    matched_subgraph_pairs = get_matching_subgraph_pairs(
        gm_a, gm_b, base_name_to_sets_of_related_ops, unmatchable_types_map
    )

    # split the subgraph pairs into one data structure for each model
    nodes_and_names_to_instrument_a: list[tuple[Node, str]] = []
    nodes_and_names_to_instrument_b: list[tuple[Node, str]] = []
    for match_name, match in matched_subgraph_pairs.items():
        subgraph_a, subgraph_b = match
        nodes_and_names_to_instrument_a.append((subgraph_a.base_op_node, match_name))
        nodes_and_names_to_instrument_b.append((subgraph_b.base_op_node, match_name))

    # populate the results, one model at a time
    results: NSResultsType = {}
    _extract_weights_one_model(
        model_name_a,
        gm_a,
        nodes_and_names_to_instrument_a,
        results,
        op_to_type_to_weight_extraction_fn,
    )
    _extract_weights_one_model(
        model_name_b,
        gm_b,
        nodes_and_names_to_instrument_b,
        results,
        op_to_type_to_weight_extraction_fn,
    )

    # fill in missing fqn entries
    maybe_add_missing_fqns(results)

    # rekey on names of nodes in gm_b
    results = rekey_logger_info_on_node_name_of_model(results, model_name_b)

    return results

