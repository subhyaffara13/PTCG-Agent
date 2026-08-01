
def _convert_fx(
    graph_module: GraphModule,
    is_reference: bool,
    convert_custom_config: ConvertCustomConfig | dict[str, Any] | None = None,
    is_standalone_module: bool = False,
    _remove_qconfig: bool = True,
    qconfig_mapping: QConfigMapping | dict[str, Any] | None = None,
    backend_config: BackendConfig | dict[str, Any] | None = None,
    is_decomposed: bool = False,
    keep_original_weights: bool = False,
) -> GraphModule:
    """`is_standalone_module`: see docs in :func:`~torch.ao.quantization.prepare_standalone_module_fx`"""
    if convert_custom_config is None:
        convert_custom_config = ConvertCustomConfig()

    if isinstance(convert_custom_config, dict):
        warnings.warn(
            "Passing a convert_custom_config_dict to convert is deprecated and will not be supported "
            "in a future version. Please pass in a ConvertCustomConfig instead.",
            FutureWarning,
            stacklevel=3,
        )
        convert_custom_config = ConvertCustomConfig.from_dict(convert_custom_config)

    _check_is_graph_module(graph_module)
    preserved_attr_names = convert_custom_config.preserved_attributes
    preserved_attrs = {
        attr: getattr(graph_module, attr)
        for attr in preserved_attr_names
        if hasattr(graph_module, attr)
    }

    quantized = convert(
        graph_module,
        is_reference,
        convert_custom_config,
        is_standalone_module,
        _remove_qconfig_flag=_remove_qconfig,
        qconfig_mapping=qconfig_mapping,
        backend_config=backend_config,
        is_decomposed=is_decomposed,
        keep_original_weights=keep_original_weights,
    )

    attach_preserved_attrs_to_model(quantized, preserved_attrs)
    return quantized

