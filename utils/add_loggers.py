
def add_loggers(
    name_a: str,
    model_a: nn.Module,
    name_b: str,
    model_b: nn.Module,
    logger_cls: Callable,
    should_log_inputs: bool = False,
    base_name_to_sets_of_related_ops: dict[str, set[NSNodeTargetType]] | None = None,
    unmatchable_types_map: dict[str, set[NSNodeTargetType]] | None = None,
) -> tuple[nn.Module, nn.Module]:
    """
    Instrument model A and model B with loggers.

    Args:
        name_a: string name of model A to use in results
        model_a: model A
        name_b: string name of model B to use in results
        model_b: model B
        logger_cls: class of Logger to use
        base_name_to_sets_of_related_ops: optional override of subgraph base nodes, subject to change
        unmatchable_types_map: optional override of unmatchable types, subject to change

    Return:
        Returns a tuple of (model_a_with_loggers, model_b_with_loggers).  Modifies both models inplace.
    """

    torch._C._log_api_usage_once("quantization_api._numeric_suite_fx.add_loggers")
    # TODO(future PR): expose these
    skipped_module_names: list[str] = []
    skipped_module_classes: list[Callable] = []
    tracer_a = NSTracer(skipped_module_names, skipped_module_classes)
    tracer_b = NSTracer(skipped_module_names, skipped_module_classes)
    gm_a = GraphModule(model_a, tracer_a.trace(model_a))
    maybe_model_a_node_name_to_scope = _get_observed_graph_module_attr(
        model_a, "node_name_to_scope"
    )
    if maybe_model_a_node_name_to_scope is not None:
        gm_a._node_name_to_scope = maybe_model_a_node_name_to_scope
    gm_b = GraphModule(model_b, tracer_b.trace(model_b))
    maybe_model_b_node_name_to_scope = _get_observed_graph_module_attr(
        model_b, "node_name_to_scope"
    )
    if maybe_model_b_node_name_to_scope is not None:
        gm_b._node_name_to_scope = maybe_model_b_node_name_to_scope
    return _add_loggers_impl(
        name_a,
        gm_a,
        name_b,
        gm_b,
        logger_cls,
        should_log_inputs=should_log_inputs,
        base_name_to_sets_of_related_ops=base_name_to_sets_of_related_ops,
        unmatchable_types_map=unmatchable_types_map,
    )

