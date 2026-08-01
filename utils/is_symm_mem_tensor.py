
def is_symm_mem_tensor(tensor: torch.Tensor) -> bool:
    r"""
    is_symm_mem_tensor(tensor) -> bool

    Returns ``True`` if ``tensor`` was allocated via symmetric memory
    (i.e. via :func:`torch.distributed._symmetric_memory.empty` or
    :meth:`_SymmetricMemory.empty_strided_p2p`).

    This is a non-collective, O(1) check.

    Args:
        tensor (:class:`torch.Tensor`): the tensor to check.
    """
    return _SymmetricMemory.is_symm_mem_tensor(tensor)

