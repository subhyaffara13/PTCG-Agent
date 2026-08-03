from typing import Any

def _prepare_fx(
    model: torch.nn.Module,
    qconfig_mapping: QConfigMapping | dict[str, Any],
    is_qat: bool,
    example_inputs: tuple[Any, ...],
    prepare_custom_config: PrepareCustomConfig | dict[str, Any] | None = None,
    _equalization_config: QConfigMapping | dict[str, Any] | None = None,
    backend_config: BackendConfig | dict[str, Any] | None = None,
    is_standalone_module: bool = False,
) -> GraphModule:
    r"""Internal helper function for prepare_fx
        Args:
          `model`, `qconfig_mapping`, `prepare_custom_config`, `_equalization_config`:
          see docs for :func:`~torch.ao.quantization.prepare_fx`
          `is_standalone_module`: a boolean flag indicates whether we are
          quantizing a standalone module or not, a standalone module
          is a submodule of the parent module that is not inlined in the
    forward graph of the parent module,
          the way we quantize standalone module is described in:
          :func:`~torch.ao.quantization._prepare_standalone_module_fx`
    """
    if prepare_custom_config is None:
        prepare_custom_config = PrepareCustomConfig()
    if _equalization_config is None:
        _equalization_config = QConfigMapping()

    if isinstance(prepare_custom_config, dict):
        warnings.warn(
            "Passing a prepare_custom_config_dict to prepare is deprecated and will not be supported "
            "in a future version. Please pass in a PrepareCustomConfig instead.",
            FutureWarning,
            stacklevel=3,
        )
        prepare_custom_config = PrepareCustomConfig.from_dict(prepare_custom_config)

    # swap FloatFunctional with FXFloatFunctional
    _swap_ff_with_fxff(model)

    skipped_module_names, skipped_module_classes = get_skipped_module_name_and_classes(
        prepare_custom_config, is_standalone_module
    )
    preserved_attr_names = prepare_custom_config.preserved_attributes
    preserved_attrs = {
        attr: getattr(model, attr)
        for attr in preserved_attr_names
        if hasattr(model, attr)
    }
    # symbolically trace the model
    tracer = QuantizationTracer(skipped_module_names, skipped_module_classes)  # type: ignore[arg-type]
    graph_module = GraphModule(model, tracer.trace(model))
    _attach_meta_to_node_if_not_exist(graph_module)

    fuse_custom_config = FuseCustomConfig().set_preserved_attributes(
        prepare_custom_config.preserved_attributes
    )
    graph_module = _fuse_fx(graph_module, is_qat, fuse_custom_config, backend_config)
    prepared = prepare(
        graph_module,
        qconfig_mapping,
        is_qat,
        tracer.node_name_to_scope,
        example_inputs=example_inputs,
        prepare_custom_config=prepare_custom_config,
        _equalization_config=_equalization_config,
        backend_config=backend_config,
        is_standalone_module=is_standalone_module,
    )  # type: ignore[operator]

    attach_preserved_attrs_to_model(prepared, preserved_attrs)
    return prepared

