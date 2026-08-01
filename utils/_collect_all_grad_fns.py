
def _collect_all_grad_fns(tensor: torch.Tensor) -> set[torch.autograd.graph.Node]:
    from torch._subclasses.fake_tensor import get_plain_tensors
    from torch.utils._python_dispatch import is_traceable_wrapper_subclass

    grad_fns: set[torch.autograd.graph.Node] = set()

    plain_tensors: list[torch.SymInt | torch.Tensor | int | OpaqueBase] = []
    # Get all plain tensors (handles nested subclasses)
    if is_traceable_wrapper_subclass(tensor):
        get_plain_tensors(tensor, out=plain_tensors)
    else:
        plain_tensors.append(tensor)

    for t in plain_tensors:
        if not isinstance(t, torch.Tensor):
            continue

        if t.grad_fn is not None:
            grad_fns.add(t.grad_fn)

        # For views, also include the base tensor's grad_fn
        if t._base is not None and t._base.grad_fn is not None:
            grad_fns.add(t._base.grad_fn)

    return grad_fns

