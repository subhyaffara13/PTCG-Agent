
def normal_(
    tensor: torch.Tensor, mean: float = 0.0, std: float = 1.0, generator: torch.Generator | None = None
) -> torch.Tensor:
    if not getattr(tensor, "_is_hf_initialized", False):
        return TORCH_INIT_FUNCTIONS["normal_"](tensor, mean=mean, std=std, generator=generator)
    return tensor


def normal_(
    key: torch.Tensor,
    result: torch.Tensor,
    *,
    mean: float = 0.0,
    std: float = 1.0,
) -> torch.Tensor:
    r"""Fill ``result`` in-place with normal random values from a PRNG key.

    The values are drawn from a normal distribution with the specified ``mean``
    and ``std``. The output is fully determined by the key, so calling with the
    same key always produces the same result.

    Supports batched keys: if ``key`` has shape ``(*batch, K)``, the leading
    dimensions of ``result`` must be broadcastable with ``*batch`` and each key
    independently generates its slice of the output.

    Args:
        key (Tensor): A PRNG key returned by :func:`key`, :func:`split`, or
            :func:`fold_in`.
        result (Tensor): The output tensor to fill in-place.
        mean (float): Mean of the normal distribution. Default: ``0.0``.
        std (float): Standard deviation of the normal distribution. Default: ``1.0``.

    Returns:
        ``result``, filled with normal random values.

    Example::

        >>> key = torch.func._random.key(42, device="cuda")  # doctest: +SKIP
        >>> result = torch.empty(1000, device="cuda")  # doctest: +SKIP
        >>> torch.func._random.normal_(key, result)  # doctest: +SKIP
    """
    return torch.ops.aten._philox_normal_(result, key, mean, std)


def normal_(
    tensor: Tensor,
    mean: float = 0.0,
    std: float = 1.0,
    generator: torch.Generator | None = None,
) -> Tensor:
    r"""Fill the input Tensor with values drawn from the normal distribution.

    :math:`\mathcal{N}(\text{mean}, \text{std}^2)`.

    Args:
        tensor: an n-dimensional `torch.Tensor`
        mean: the mean of the normal distribution
        std: the standard deviation of the normal distribution
        generator: the torch Generator to sample from (default: None)

    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.normal_(w)
    """
    if torch.overrides.has_torch_function_variadic(tensor):
        return torch.overrides.handle_torch_function(
            normal_, (tensor,), tensor=tensor, mean=mean, std=std, generator=generator
        )
    return _no_grad_normal_(tensor, mean, std, generator)


def normal_(self, mean=0, std=1, *, generator=None):
    return normal(mean, std, self.shape, out=self, generator=generator)


def normal_(types, args=(), kwargs=None, pg=None):
    r"""
    Fills the Tensors in tensor.local_shards with values drawn from the normal
    distribution :math:`\mathcal{N}(\text{mean}, \text{std}^2)`.
    Args:
        tensor: tensor sharded across devices
        mean: the mean of the normal distribution
        std: the standard deviation of the normal distribution
    """
    validate_param(kwargs, "kwargs")
    # pyrefly: ignore [unsupported-operation]
    sharded_tensor = kwargs["tensor"]
    validate_param(sharded_tensor, "tensor")
    # pyrefly: ignore [unsupported-operation]
    mean = kwargs["mean"]
    validate_param(mean, "mean")
    # pyrefly: ignore [unsupported-operation]
    std = kwargs["std"]
    validate_param(std, "std")

    for shard in sharded_tensor.local_shards():
        torch.nn.init.normal_(shard.tensor, mean=mean, std=std)
    return sharded_tensor

