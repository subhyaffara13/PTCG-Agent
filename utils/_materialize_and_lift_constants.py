
def _materialize_and_lift_constants(
    gm: torch.fx.GraphModule,
    export_graph_signature: ExportGraphSignature,
    constant_attrs: ConstantAttrMap,
) -> dict[str, _ConstantAttributeType]:
    constants = rewrite_script_object_meta(gm)
    constants.update(lift_constants_pass(gm, export_graph_signature, constant_attrs))
    return constants

