
def _lower_to_native_backend(
    model: GraphModule,
    qconfig_map: dict[str, QConfigAny],
    node_name_to_scope: dict[str, tuple[str, type]],
    keep_original_weights: bool = False,
) -> GraphModule:
    """Lower a quantized reference model (with reference quantized operator patterns)
    to the native backend in PyTorch (fbgemm/qnnpack), both backends shares the same
    operator signature so they can be lowered with the same function
    """
    _lower_static_weighted_ref_module(model, qconfig_map)
    _lower_static_weighted_ref_module_with_two_inputs(model, qconfig_map)
    _lower_dynamic_weighted_ref_module(model)
    _lower_weight_only_weighted_ref_module(model)
    _lower_static_weighted_ref_functional(model, qconfig_map)
    _lower_dynamic_weighted_ref_functional(model, qconfig_map)
    _lower_quantized_binary_op(model, qconfig_map)
    _lower_getattr_tensor_metadta_op(model)
    _lower_get_tensor_info_op(model)
    special_pattern_replacement(model)
    model.graph.eliminate_dead_code()
    model = fold_weight(model, node_name_to_scope, keep_original_weights)
    model.graph.eliminate_dead_code()
    model.recompile()
    model.graph.lint()
    return model

