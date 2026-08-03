from typing import Any

def custom_function_call_vmap_generate_rule(
    interpreter: VmapInterpreter,
    autograd_function: type[torch.autograd.Function],
    *operands: Any,
) -> Any:
    unwrapped_operands, in_dims = unwrap_batched(operands, interpreter.level())
    vmapped_function = vmapify_autograd_function(
        autograd_function,
        in_dims,
        interpreter.batch_size(),
        interpreter.randomness(),
    )
    with interpreter.lower():
        outputs = custom_function_call(vmapped_function, *unwrapped_operands)

    if not isinstance(outputs, tuple):
        raise AssertionError(f"expected outputs to be a tuple, got {type(outputs)}")
    outputs, out_dims = unpack_outputs(outputs)
    return wrap_batched(outputs, out_dims, interpreter.level())

