
def zeros_(tensor: torch.Tensor) -> torch.Tensor:
    if not getattr(tensor, "_is_hf_initialized", False):
        return TORCH_INIT_FUNCTIONS["zeros_"](tensor)
    return tensor


def zeros_(tensor: Tensor) -> Tensor:
    r"""Fill the input Tensor with the scalar value `0`.

    Args:
        tensor: an n-dimensional `torch.Tensor`

    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.zeros_(w)
    """
    return _no_grad_zero_(tensor)

