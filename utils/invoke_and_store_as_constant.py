
def invoke_and_store_as_constant(
    tx: "InstructionTranslator",
    fn: Callable[..., Any],
    name: str,
    args: Sequence[VariableTracker],
    kwargs: dict[str, VariableTracker],
) -> VariableTracker:
    def convert(x: VariableTracker) -> Any:
        if x.is_tensor():
            return cast("TensorVariable", x).get_real_value()
        if isinstance(x, UserDefinedObjectVariable):
            if x.source is not None:
                install_guard(x.make_guard(GuardBuilder.ID_MATCH))
            return x.value
        try:
            return x.as_python_constant()
        except AsPythonConstantNotImplementedError:
            unimplemented(
                gb_type="assume_constant_result argument conversion failed",
                context=f"function {name}, variable type {type(x).__name__}",
                explanation=f"Cannot convert argument of type {type(x).__name__} to a Python constant "
                f"for function {name} marked with torch._dynamo.assume_constant_result. "
                f"The variable tracker does not support constant conversion.",
                hints=[
                    "Remove torch._dynamo.assume_constant_result from this function",
                    "Ensure all arguments passed to the function can be converted to constants",
                ],
            )

    args = [convert(x) for x in args]
    kwargs = {k: convert(v) for k, v in kwargs.items()}
    res = fn(*args, **kwargs)
    return tx.output.register_attr_or_module(
        res,
        name,
        source=ConstantSource(name),
    )

