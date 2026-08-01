
def ones_(tensor: torch.Tensor) -> torch.Tensor:
    if not getattr(tensor, "_is_hf_initialized", False):
        return TORCH_INIT_FUNCTIONS["ones_"](tensor)
    return tensor


def ones_(tensor: Tensor) -> Tensor:
    r"""Fill the input Tensor with the scalar value `1`.

    Args:
        tensor: an n-dimensional `torch.Tensor`

    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.ones_(w)
    """
    return _no_grad_fill_(tensor, 1.0)

