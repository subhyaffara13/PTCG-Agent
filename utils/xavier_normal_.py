
def xavier_normal_(tensor: torch.Tensor, gain: float = 1.0, generator: torch.Generator | None = None) -> torch.Tensor:
    if not getattr(tensor, "_is_hf_initialized", False):
        return TORCH_INIT_FUNCTIONS["xavier_normal_"](tensor, gain=gain, generator=generator)
    return tensor


def xavier_normal_(
    tensor: Tensor,
    gain: float = 1.0,
    generator: torch.Generator | None = None,
) -> Tensor:
    r"""Fill the input `Tensor` with values using a Xavier normal distribution.

    The method is described in `Understanding the difficulty of training deep feedforward
    neural networks` - Glorot, X. & Bengio, Y. (2010). The resulting tensor
    will have values sampled from :math:`\mathcal{N}(0, \text{std}^2)` where

    .. math::
        \text{std} = \text{gain} \times \sqrt{\frac{2}{\text{fan\_in} + \text{fan\_out}}}

    Also known as Glorot initialization.

    Args:
        tensor: an n-dimensional `torch.Tensor`
        gain: an optional scaling factor
        generator: the torch Generator to sample from (default: None)

    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.xavier_normal_(w)
    """
    fan_in, fan_out = _calculate_fan_in_and_fan_out(tensor)
    std = gain * math.sqrt(2.0 / float(fan_in + fan_out))

    return _no_grad_normal_(tensor, 0.0, std, generator)

