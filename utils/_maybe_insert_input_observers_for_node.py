
def _maybe_insert_input_observers_for_node(
    node: Node,
    qconfig: QConfigAny,
    model: torch.nn.Module,
    named_modules: dict[str, torch.nn.Module],
    graph: Graph,
    qhandler: QuantizeHandler | None,
    prepare_custom_config: PrepareCustomConfig,
    obs_or_fq_map: dict[EdgeOrNode, ObserverOrFakeQuantize],
    is_qat: bool,
    backend_config: BackendConfig | None = None,
    model_device: torch.device | None = None,
) -> None:
    """
    If needed, inserts observers to the input args and kwargs of `node`.
    Note: modifies `node` inplace.

    For example, if cur_node needs an observer after prev_node, we change from

      prev_node -> cur_node

    To

      prev_node -> obs -> cur_node

    Note: backend_config only needed for standalone_module node
    """
    # Look through every input arg.  If that arg's target dtype does not
    # match the current node's target dtype, insert an observer.
    new_args = []
    for arg in node.args:
        new_arg = _maybe_insert_input_observer_for_arg_or_kwarg(
            node,
            arg,
            qconfig,
            model,
            named_modules,
            graph,
            qhandler,
            prepare_custom_config,
            obs_or_fq_map,
            is_qat,
            backend_config,
            model_device,
        )
        new_args.append(new_arg)

    new_kwargs = {}
    for k, kwarg in node.kwargs.items():
        new_kwarg = _maybe_insert_input_observer_for_arg_or_kwarg(
            node,
            kwarg,
            qconfig,
            model,
            named_modules,
            graph,
            qhandler,
            prepare_custom_config,
            obs_or_fq_map,
            is_qat,
            backend_config,
            model_device,
        )
        new_kwargs[k] = new_kwarg

    # assign the new args and kwargs to the node, inplace
    node.args = tuple(new_args)
    node.kwargs = new_kwargs

