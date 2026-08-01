
def _check_supported_callable_arg(
    tx: "InstructionTranslator", func_var: VariableTracker, arg_name: str
) -> None:
    from .builder import SourcelessBuilder

    is_callable = (
        SourcelessBuilder.create(tx, callable)
        .call_function(tx, [func_var], {})
        .as_python_constant()
    )
    if not is_callable:
        unimplemented(
            gb_type="HOP: non-callable variable",
            context=f"arg name: {arg_name}, func_var type: {str(func_var)}",
            explanation=f"{arg_name} should be a callable but is of type {str(func_var)}.",
            hints=[],
        )

