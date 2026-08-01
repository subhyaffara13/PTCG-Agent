
def dispatch_functorch(op: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    interpreter = retrieve_current_functorch_interpreter()
    # In traditional PyTorch operators, DispatchKey::FuncTorchTensorWrapper's
    # unwrap_dead_tensors fallback handles unwrapping dead tensor wrappers.
    # PyDispatcher sidesteps the PyTorch dispatcher when dealing with functorch
    # transforms, so we manually unwrap the dead tensors here.
    # This logic won't need to exist when we have mode-only functorch.
    args, kwargs = pytree.tree_map_only(
        torch.Tensor, torch._C._functorch.unwrap_if_dead, (args, kwargs)
    )
    return interpreter.process(op, args, kwargs)

