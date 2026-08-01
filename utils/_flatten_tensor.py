
def _flatten_tensor(
    tensor: torch.Tensor,
) -> tuple[torch.Tensor, DTensorSpec | None]:
    if isinstance(tensor, DTensor):
        tensor._local_tensor.requires_grad_()
        return tensor._local_tensor, tensor._spec
    return tensor, None


def _flatten_tensor(tensor):
    "Depth-first iterator over scalars in a tensor."
    iterator = iter(tensor)
    while True:
        try:
            value = next(iterator)
        except StopIteration:
            return iterator
        iterator = chain((value,), iterator)
        if _is_scalar(value):
            return iterator
        iterator = chain.from_iterable(iterator)

