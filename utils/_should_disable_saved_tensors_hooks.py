
def _should_disable_saved_tensors_hooks() -> bool:
    # Compiled autograd is not supported yet, to be added in future.
    if torch._dynamo.compiled_autograd.in_compiled_autograd_region:
        return False

    get_hooks = torch._functorch._aot_autograd.utils.top_saved_tensors_hooks
    are_inline_hooks = (
        torch._functorch._aot_autograd.utils.saved_tensors_hooks_are_inlineable
    )

    hooks = get_hooks()
    if are_inline_hooks(hooks):
        return True

    return False

