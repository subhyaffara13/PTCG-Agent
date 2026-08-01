
def new_parameter_placeholder(
    size: tuple[int, ...], dtype: torch.dtype, device: torch.device, requires_grad: bool
) -> torch.nn.Parameter:
    """Create a placeholder to be passed to the above functions"""
    result = torch.nn.Parameter(
        torch.empty(size, dtype=dtype, device=device), requires_grad=requires_grad
    )
    # TODO(jansel): alloc followed by free is inefficient, need a way to allocate an unbacked tensor.
    # Allocating a zero tensor would causes assert failures in autograd.
    result.untyped_storage().resize_(0)
    return result

