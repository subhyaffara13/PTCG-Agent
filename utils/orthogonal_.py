
def orthogonal_(
    tensor: torch.Tensor,
    gain: float = 1,
    generator: torch.Generator | None = None,
) -> torch.Tensor:
    if not getattr(tensor, "_is_hf_initialized", False):
        return TORCH_INIT_FUNCTIONS["orthogonal_"](tensor, gain=gain, generator=generator)
    return tensor


def orthogonal_(
    tensor: Tensor,
    gain: float = 1,
    generator: torch.Generator | None = None,
) -> Tensor:
    r"""Fill the input `Tensor` with a (semi) orthogonal matrix.

    Described in `Exact solutions to the nonlinear dynamics of learning in deep
    linear neural networks` - Saxe, A. et al. (2013). The input tensor must have
    at least 2 dimensions, and for tensors with more than 2 dimensions the
    trailing dimensions are flattened.

    Args:
        tensor: an n-dimensional `torch.Tensor`, where :math:`n \geq 2`
        gain: optional scaling factor
        generator: the torch Generator to sample from (default: None)

    Examples:
        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_LAPACK)
        >>> w = torch.empty(3, 5)
        >>> nn.init.orthogonal_(w)
    """
    if tensor.ndimension() < 2:
        raise ValueError("Only tensors with 2 or more dimensions are supported")

    if tensor.numel() == 0 or tensor.is_meta:
        # no-op
        return tensor
    rows = tensor.size(0)
    cols = tensor.numel() // rows
    flattened = tensor.new_empty((rows, cols)).normal_(0, 1, generator=generator)

    if rows < cols:
        flattened.t_()

    # Compute the qr factorization
    q, r = torch.linalg.qr(flattened)
    # Make Q uniform according to https://arxiv.org/pdf/math-ph/0609050.pdf
    d = torch.diag(r, 0)
    ph = d.sign()
    q *= ph

    if rows < cols:
        q.t_()

    with torch.no_grad():
        tensor.view_as(q).copy_(q)
        tensor.mul_(gain)
    return tensor

