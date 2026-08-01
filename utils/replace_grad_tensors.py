
def replace_grad_tensors(output: Any, tensor_iter: Iterator[torch.Tensor]) -> Any:
    """
    Replace grad-requiring tensors in a nested structure using replacements
    from tensor_iter.

    Tensors are consumed from tensor_iter in the same traversal order as
    :func:`collect_grad_tensors`. Traverses dict, list, tuple, NamedTuple,
    and dataclass containers; sets and other iterables are *not* traversed
    (consistent with ``tree_flatten``).

    Note: dataclass reconstruction uses ``dataclasses.replace()``, which calls
    ``__init__``. Dataclasses with custom ``__init__`` validation,
    ``__post_init__`` side effects, or non-standard dict subclass constructors
    may not be compatible. In practice, FSDP module outputs are expected to be
    shallowly nested, so recursion depth is not a concern.
    """
    result = _replace_grad_tensors(output, tensor_iter)
    sentinel = object()
    leftover = next(tensor_iter, sentinel)
    if leftover is not sentinel:
        # Count remaining without holding references to all of them
        n = 1 + sum(1 for _ in tensor_iter)
        raise RuntimeError(
            f"{n} replacement tensors were not consumed while processing "
            f"{type(output).__qualname__}"
        )
    return result

