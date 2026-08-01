
def handle_dispatch_mode(curr_mode, op_overload, *args, **kwargs):
    if not isinstance(curr_mode, torch.utils._python_dispatch.TorchDispatchMode):
        raise AssertionError(
            f"curr_mode must be TorchDispatchMode, got {type(curr_mode)}"
        )
    args_flattened, _ = torch.utils._pytree.tree_flatten((args, kwargs.values()))
    # TODO: need to double check the semantics of the "types" argument to torch_dispatch.
    # It's generated in PyInterpreter.cpp, but seems to be generated in two places,
    # where in one case we only include tensors with the python key, and in another
    # we include **all** tensors.
    overload_types = [
        type(a)
        for a in args_flattened
        if isinstance(a, torch.Tensor)
        and torch._C._dispatch_keys(a).has(torch._C.DispatchKey.Python)
    ]
    # TODO: check that I got these args correct (in C++, we pass in "0000"??)

    return curr_mode.__torch_dispatch__(op_overload, overload_types, args, kwargs)

