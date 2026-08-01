
def assert_view_op_properties(func: FunctionSchema) -> None:
    def is_alias(a: Argument) -> bool:
        return a.annotation is not None

    args = func.arguments.flat_non_out
    # The first argument is a tensor with an alias semantics (annotations)
    if not (len(args) > 0 and args[0].type == BaseType(BaseTy.Tensor)):
        raise AssertionError(
            f"In the functionalization codegen, we expect the first argument of every view operator to be a tensor, "
            f"but found an argument of type {str(args[0].type)} for operator: {str(func.name)}."
        )
    # No other arguments have aliasing semantics
    if not (is_alias(args[0]) and not any(is_alias(a) for a in args[1:])):
        raise AssertionError(
            "In the functionalization codegen, we expect the first argument of every view "
            "operator to alias the output. View operators with multiple aliasing inputs "
            "aren't supported yet. Found an operator that doesn't satisfy this constraint"
        )

