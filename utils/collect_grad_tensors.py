
def collect_grad_tensors(output: Any) -> tuple[torch.Tensor, ...]:
    """
    Recursively collect tensors that require gradients from a nested structure.

    Traverses dict, list, tuple, NamedTuple, and dataclass containers.
    Sets and other iterables are *not* traversed (consistent with
    ``tree_flatten``).  Uses the same traversal order as
    :func:`replace_grad_tensors`.
    """
    tensors_list: list[torch.Tensor] = []
    _collect_grad_tensors(output, tensors_list)
    return tuple(tensors_list)

