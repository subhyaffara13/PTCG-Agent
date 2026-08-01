
def _remap_constants(
    orig_constant_attrs: ConstantAttrMap,
    graph_signature: ExportGraphSignature,
    constants: dict[str, _ConstantAttributeType],
) -> None:
    """Rewrite the graph signature and constants table to use the FQN from the original module."""
    remap_table: dict[str, list[str]] = {}
    for name, value in constants.items():
        if value in orig_constant_attrs:
            remap_table[name] = orig_constant_attrs[value]

    for spec in graph_signature.input_specs:
        if spec.kind in (
            InputKind.CONSTANT_TENSOR,
            InputKind.CUSTOM_OBJ,
        ):
            orig_target = spec.target
            if orig_target is None:
                raise AssertionError(
                    f"spec.target must not be None for kind {spec.kind}"
                )
            targets = remap_table.get(orig_target, [orig_target])
            spec.target = targets[0]

            constant = constants[orig_target]
            del constants[orig_target]
            for target in targets:
                constants[target] = constant

