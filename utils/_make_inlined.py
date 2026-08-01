
def _make_inlined(
    tx: InstructionTranslator, f: Callable[..., Any]
) -> Callable[..., VariableTracker]:
    assert callable(f), "Expect f to be a python callable."

    def inline_call(
        *args: VariableTracker, **kwargs: VariableTracker
    ) -> VariableTracker:
        from torch._dynamo.trace_rules import _force_inline
        from torch._dynamo.variables.functions import UserFunctionVariable

        with _force_inline():
            return UserFunctionVariable(f).call_function(tx, args, kwargs)  # type: ignore[arg-type]

    return inline_call

