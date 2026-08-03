from typing import Any, Callable

def custom_function_call_vmap_helper(
    interpreter: VmapInterpreter,
    vmap_function: Callable[..., Any],
    op: Any,
    *operands: Any,
    **kwargs: Any,
) -> Any:
    current_level = interpreter.level()
    info = VmapInfo(
        batch_size=interpreter.batch_size(),
        randomness=interpreter.randomness(),
    )
    # We're either in the autograd.Function case (vmap staticmethod)
    # or the torch.library.register_vmap case.
    autograd_function_case = isinstance(op, torch.autograd.function.FunctionMeta)

    def lower_to_next() -> Any:
        if autograd_function_case:
            return interpreter.lower()
        else:
            return torch._C._ExcludeDispatchKeyGuard(
                torch._C.DispatchKeySet(torch._C.DispatchKey.FuncTorchBatched)
            )

    unwrapped_operands, in_dims = unwrap_batched(operands, current_level)
    # If none of the tensors are batched at the current level, then we skip the
    # current level. This saves the user from needing to handle this case in
    # their vmap staticmethod (and is consistent with our C++ batching rule API)
    if pytree.tree_all(lambda dim: dim is None, in_dims):
        with lower_to_next():
            if autograd_function_case:
                return custom_function_call(op, *operands)
            else:
                return op(*operands, **kwargs)

    with lower_to_next():
        result = vmap_function(info, in_dims, *unwrapped_operands, **kwargs)
    validate_vmap_returns_tuple_of_two_elements(result)
    unwrapped_output, out_dims = result

    # See NOTE [mark_dirty object identity check]
    def wrap_fn(output: torch.Tensor, out_dim: int | None) -> torch.Tensor:
        return (
            output
            if out_dim is None
            else _add_batch_dim(output, out_dim, current_level)
        )

    return wrap_outputs_maintaining_identity(
        unwrapped_output, unwrapped_operands, operands, wrap_fn, out_dims=out_dims
    )

