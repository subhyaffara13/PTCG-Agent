from typing import Any

def _fakify_module_inputs(
    args: tuple[Any],
    kwargs: dict[Any, Any],
    fake_mode: torch._subclasses.fake_tensor.FakeTensorMode,
):
    # This context manager is used to fakify module inputs.
    # Inputs:
    #   args, kwargs: the args and kwargs containing module inputs that haven't been fakified.
    #   fake_mode: the fake mode to be used for fakifying script objects. It's the same mode that fakify input tensors.

    ctxs = [_enable_graph_inputs_of_type_nn_module((args, kwargs))]
    for arg in pytree.tree_leaves((args, kwargs)):
        if isinstance(arg, torch.nn.Module):
            fake_params_buffers = _fakify_params_buffers(fake_mode, arg)
            ctxs.append(
                torch.nn.utils.stateless._reparametrize_module(
                    arg,
                    fake_params_buffers,
                    tie_weights=True,
                    strict=True,
                    stack_weights=True,
                )
            )
    with contextlib.ExitStack() as stack:
        for ctx in ctxs:
            stack.enter_context(ctx)
        yield

