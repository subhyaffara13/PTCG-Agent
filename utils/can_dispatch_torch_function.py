
def can_dispatch_torch_function(
    tx: "InstructionTranslator", args: Iterable[Any], kwargs: dict[str, Any]
) -> bool:
    has_overridden_args = any(
        has_torch_function(arg) for arg in _get_all_args(args, kwargs)
    )
    tf_state = tx.symbolic_torch_function_state
    return (has_overridden_args and tf_state.torch_function_subclass_enabled) or (
        tf_state.torch_function_mode_enabled and tf_state.in_torch_function_mode()
    )

