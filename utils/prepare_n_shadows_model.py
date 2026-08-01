
def prepare_n_shadows_model(
    model: torch.nn.Module,
    example_inputs: Any,
    qconfig_multi_mapping: QConfigMultiMapping,
    backend_config: BackendConfig,
    custom_prepare_fn: Callable | None = None,
    custom_prepare_kwargs: dict[str, Any] | None = None,
    custom_tracer: Any = None,
) -> GraphModule:
    """
    Given a model with a graph with M ops such as


      args_kwargs_m -> op_m -> output_m


    And a set of N qconfigs for each op, creates a new model, with
    each of the subgraph of `op_m` transformed into

    .. code::

           |---------> op_m_n -> log_m_n
           |                     /
      args_kwargs_m ---------> op_m -> log_m_0

    Where op_m_n is op_m wrapped in a submodule and transformed with
    qconfig_n, and its inner graph looks like

    .. code::

      args_m -------- op_m_prepared_with_qconfig_n -> out_m_n
                  /
      kwargs_m ---

    This is useful for testing different quantization of multiple layers in
    a single pass through the model.

    High level TODOs for future PRs:
    * figure out a better way to name the output structure
    * return a results data structure instead of printing it out
    * add examples to docblocks
    """

    if custom_tracer is None:
        tracer = quantize_fx.QuantizationTracer([], [])
    else:
        tracer = custom_tracer
    mt = torch.fx.GraphModule(model, tracer.trace(model))
    # this is necessary to ensure logger FQNs get populated
    mt._node_name_to_scope = tracer.node_name_to_scope  # type: ignore[assignment]

    # run example input propagation, we need this to call prepare_fx on
    # individual subgraphs
    output_prop = OutputProp(mt)
    output_prop.propagate(*example_inputs)

    # Find the set of subgraphs in the original graph which we need to
    # consider.
    modules = dict(mt.named_modules(remove_duplicate=False))
    patterns = _get_pattern_to_quantize_handlers(backend_config)
    root_node_getter_mapping = get_fusion_pattern_to_root_node_getter(backend_config)
    standalone_module_names: list[str] = []
    standalone_module_classes: list[type] = []
    custom_module_classes: list[type] = []
    matches = _find_matches(
        mt.graph,
        modules,
        patterns,
        root_node_getter_mapping,
        standalone_module_names,
        standalone_module_classes,
        custom_module_classes,
    )
    subgraphs_dedup: dict[str, list[Node]] = _get_dedup_subgraphs(matches)

    # generate node to qconfig for each subgraph
    # TODO(future PR): deduplicate repeating entries
    list_of_node_name_to_qconfig: list[dict[str, QConfigAny]] = []
    for qconfig_mapping in qconfig_multi_mapping.qconfig_mappings_list:
        node_name_to_qconfig = _generate_node_name_to_qconfig(
            mt, modules, mt.graph, qconfig_mapping, tracer.node_name_to_scope
        )
        list_of_node_name_to_qconfig.append(node_name_to_qconfig)

    # For each region in the model, do the following:
    #   For each qconfig for that region, do the following:
    #     1. create a copy of the region wrapped in a module
    #     2. pass original args, original kwargs, and expected output to module
    #     3. add an output comparison logger and hook it up to compare
    #        actual output to expected output
    #     4. run `prepare_fx` on the module
    for subgraph_idx, (match_name, nodes_in_this_subgraph) in enumerate(
        subgraphs_dedup.items()
    ):
        create_n_transformed_and_logged_copies_of_subgraph(
            mt,
            subgraph_idx,
            match_name,
            nodes_in_this_subgraph,
            qconfig_multi_mapping.qconfig_mappings_list,
            list_of_node_name_to_qconfig,
            custom_prepare_fn,
            custom_prepare_kwargs,  # type: ignore[arg-type]
        )

    return mt

