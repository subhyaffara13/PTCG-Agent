
def _collect_and_set_constant_attrs(
    graph_signature, constants, mod
) -> "ConstantAttrMap":
    # the exported module will store constants & non-persistent buffers such that
    # retracing treats them as persistent buffers, so we inform the constants lifting pass
    # and overwrite the new graph signature using the previous program. This is intended to only be used
    # in run_decompositions where we still have access to original EP.
    from torch._export.passes.lift_constants_pass import ConstantAttrMap

    constant_attrs = ConstantAttrMap()
    non_persistent_buffers = {
        spec.target
        for spec in graph_signature.input_specs
        if spec.kind == InputKind.BUFFER and not spec.persistent
    }
    for name, value in constants.items():
        if name in non_persistent_buffers:
            continue
        # recursive getattr
        _mod = mod
        *atoms, attr = name.split(".")
        for atom in atoms:
            _mod = getattr(_mod, atom)
        # remove as buffer, reassign as constant/non-persistent buffer
        _mod._buffers.pop(attr, None)
        setattr(_mod, attr, value)
        constant_attrs.add(value, name)
    return constant_attrs

