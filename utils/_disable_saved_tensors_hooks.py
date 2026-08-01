
def _disable_saved_tensors_hooks() -> Generator[None, None, None]:
    error_message = (
        "Saved tensors hooks were specialized as GraphModules."
        "In this case aot_autograd inlines them in forward and backward graph "
        "and disables them during runtime of aot_autograd compiled region."
        "If you see this error, that means that there is some unexpected push or pop manipulation "
        "during aot_autograd compiled region runtime."
        "Compilation with different hooks must result in recompilation."
    )
    fail_if_non_empty = False
    maybe_prev_message = None
    try:
        maybe_prev_message = (
            torch._C._autograd._saved_tensors_hooks_get_disabled_error_message()
        )
        torch._C._autograd._saved_tensors_hooks_disable(
            error_message, fail_if_non_empty
        )
        yield
    finally:
        if maybe_prev_message is None:
            torch._C._autograd._saved_tensors_hooks_enable()
        else:
            torch._C._autograd._saved_tensors_hooks_disable(
                maybe_prev_message, fail_if_non_empty
            )

