
def _get_logger_for_subgraph(
    model: GraphModule,
    first_node: Node,
    last_node: Node,
    subgraph_idx: int,
    subgraph_candidate_idx: int,
    qconfig_str: str,
    logger_cls: Callable,
    fqn: str | None,
) -> torch.nn.Module:
    """
    Given a model and a linear subgraph starting from `first_node` and
    ending with `last_node`, creates a logger for the end of this
    subgraph.
    """
    if fqn is None:
        fqn = ""
    logger_mod_orig = logger_cls(
        first_node.name,  # ref_node_name
        last_node.name,  # prev_node_name
        f"subgraph_{subgraph_idx}_{subgraph_candidate_idx}",  # model_name
        "model",  # ref_name
        get_target_type_str(last_node, model),  # prev_node_target_type
        get_target_type_str(first_node, model),  # ref_node_target_type
        NSSingleResultValuesType.NODE_OUTPUT.value,  # results_type
        0,  # index_within_arg
        0,  # index_of_arg
        fqn,  # fqn
        qconfig_str,
    )
    # Usually we expect the user to add loggers, then calibrate, then convert,
    # and then populate loggers.  This is why the loggers start disabled.
    # TODO(future PR): reconsider the design to make this more intuitive.
    logger_mod_orig.enabled = False
    return logger_mod_orig

