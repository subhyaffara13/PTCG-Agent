
def _run_prepare_fx_on_standalone_modules(
    model: torch.nn.Module,
    is_qat: bool,
    named_modules: dict[str, torch.nn.Module],
    node_name_to_match_result_with_qconfig: Any,
    prepare_custom_config: PrepareCustomConfig,
    backend_config: BackendConfig,
) -> None:
    """
    Runs prepare_fx on each standalone module. Note: this does
    not modify the graph, it just replaces the unobserved modules with
    their observed versions.
    """
    for (
        root_node,
        _,
        _pattern,
        qhandler,
        qconfig,
    ) in node_name_to_match_result_with_qconfig.values():
        if qhandler is None:
            continue
        elif not qhandler.is_standalone_module():
            continue

        (
            sm_qconfig_mapping,
            sm_example_inputs,
            sm_prepare_custom_config,
            sm_backend_config,
        ) = _get_standalone_module_configs(
            root_node, named_modules, prepare_custom_config, qconfig, backend_config
        )

        standalone_module = named_modules[root_node.target]
        prepare = torch.ao.quantization.quantize_fx._prepare_standalone_module_fx  # type: ignore[attr-defined]
        observed_standalone_module = prepare(
            standalone_module,
            sm_qconfig_mapping,
            is_qat,
            example_inputs=sm_example_inputs,
            prepare_custom_config=sm_prepare_custom_config,
            backend_config=sm_backend_config,
        )
        parent_name, name = _parent_name(root_node.target)
        setattr(named_modules[parent_name], name, observed_standalone_module)
        named_modules[root_node.target] = observed_standalone_module

