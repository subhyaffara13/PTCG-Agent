
def inplace_or_view_method_definition(
    fn: NativeFunctionWithDifferentiabilityInfo,
) -> str | None:
    f = fn.func
    if get_view_info(f) is None and (
        # For functions that modify their inputs but don't return them,
        # we can't give them autograd support.
        # See https://github.com/pytorch/pytorch/issues/53796
        not modifies_arguments(f) or len(f.func.returns) == 0
    ):
        return None
    return METHOD_DEFINITION.substitute(
        return_type=cpp.returns_type(f.func.returns, symint=True).cpp_type(),
        type_wrapper_name=type_wrapper_name(f),
        formals=gen_formals(f),
        type_definition_body=emit_inplace_or_view_body(fn),
    )

