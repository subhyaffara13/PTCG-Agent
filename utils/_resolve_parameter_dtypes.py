
def _resolve_parameter_dtypes(
    signature: ir.schemas.OpSignature, named_inputs: Mapping[str, AllowedArgType]
) -> Mapping[ir.schemas.TypeConstraintParam, ir.TypeProtocol]:
    """Determine which parameter takes which type.

    Handle non-tensor input corner cases and type promotion.

    Requires:
        All ir.Value in name_inputs should have type set. Their type should be
        compatible with the type_constraint of the corresponding parameter in the signature.

    Args:
        signature: The OpSignature for the node.
        named_inputs: The mapping of parameter names to their arguments.

    Returns:
        A mapping of Constraint names to ir.TypeProtocol.
    """
    #   a. Create type_binding: dict[str, ir.TypeProtocol]
    #   b. Iterate over all named_inputs
    #   b0. Find the corresponding parameter in the signature
    #   b1. If the argument is a Python constant, skip.
    #   b2. If the argument is a ir.Value, Bind {constraint: arg.type}.
    type_binding = {}
    for name, arg in named_inputs.items():
        param = signature.params_map[name]
        if not isinstance(param, ir.schemas.Parameter):
            raise AssertionError(f"Expected Parameter, got {type(param)}")
        if isinstance(arg, (int, float, bool, str, Sequence, torch.Tensor)):
            # Skip the Python constants because we do not know what dtype they should take yet
            continue
        elif isinstance(arg, ir.Value):
            if arg.type is None:
                # Skip the ir.Value if the type is not set
                continue
            # NOTE: We assume arg.type is compatible with the type_constraint
            if arg.type is None:
                raise AssertionError(f"Expected type to be set for {arg}")
            # TODO(justinchuby): Implement type promotion logic here.
            type_binding[param.type_constraint] = arg.type
    return type_binding

