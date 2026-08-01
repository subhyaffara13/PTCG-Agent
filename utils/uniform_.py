
def uniform_(
    tensor: torch.Tensor, a: float = 0.0, b: float = 1.0, generator: torch.Generator | None = None
) -> torch.Tensor:
    if not getattr(tensor, "_is_hf_initialized", False):
        return TORCH_INIT_FUNCTIONS["uniform_"](tensor, a=a, b=b, generator=generator)
    return tensor


def uniform_(
    key: torch.Tensor,
    result: torch.Tensor,
    *,
    low: float = 0.0,
    high: float = 1.0,
) -> torch.Tensor:
    r"""Fill ``result`` in-place with uniform random values from a PRNG key.

    The values are drawn uniformly from the interval ``[low, high)``. The output
    is fully determined by the key, so calling with the same key always produces
    the same result.

    Supports batched keys: if ``key`` has shape ``(*batch, K)``, the leading
    dimensions of ``result`` must be broadcastable with ``*batch`` and each key
    independently generates its slice of the output.

    Args:
        key (Tensor): A PRNG key returned by :func:`key`, :func:`split`, or
            :func:`fold_in`.
        result (Tensor): The output tensor to fill in-place.
        low (float): Lower bound (inclusive) of the uniform distribution. Default: ``0.0``.
        high (float): Upper bound (exclusive) of the uniform distribution. Default: ``1.0``.

    Returns:
        ``result``, filled with uniform random values.

    Example::

        >>> key = torch.func._random.key(42, device="cuda")  # doctest: +SKIP
        >>> result = torch.empty(1000, device="cuda")  # doctest: +SKIP
        >>> torch.func._random.uniform_(key, result)  # doctest: +SKIP
    """
    return torch.ops.aten._philox_uniform_(result, key, low, high)


def uniform_(
    tensor: Tensor,
    a: float = 0.0,
    b: float = 1.0,
    generator: torch.Generator | None = None,
) -> Tensor:
    r"""Fill the input Tensor with values drawn from the uniform distribution.

    :math:`\mathcal{U}(a, b)`.

    Args:
        tensor: an n-dimensional `torch.Tensor`
        a: the lower bound of the uniform distribution
        b: the upper bound of the uniform distribution
        generator: the torch Generator to sample from (default: None)

    Examples:
        >>> w = torch.empty(3, 5)
        >>> nn.init.uniform_(w)
    """
    if torch.overrides.has_torch_function_variadic(tensor):
        return torch.overrides.handle_torch_function(
            uniform_, (tensor,), tensor=tensor, a=a, b=b, generator=generator
        )
    return _no_grad_uniform_(tensor, a, b, generator)


def uniform_(self, low=0, high=1, generator=None):
    return self.copy_(uniform(self, low, high, generator))


def uniform_(types, args=(), kwargs=None, pg=None):
    r"""
    Fills the Tensor in tensor.local_shards with values drawn from the uniform
    distribution :math:`\mathcal{U}(a, b)`.
    Args:
        tensor: tensor sharded across devices
        a: the lower bound of the uniform distribution
        b: the upper bound of the uniform distribution
    """
    validate_param(kwargs, "kwargs")
    # pyrefly: ignore [unsupported-operation]
    sharded_tensor = kwargs["tensor"]
    validate_param(sharded_tensor, "tensor")
    # pyrefly: ignore [unsupported-operation]
    a = kwargs["a"]
    validate_param(a, "a")
    # pyrefly: ignore [unsupported-operation]
    b = kwargs["b"]
    validate_param(b, "b")

    for shard in sharded_tensor.local_shards():
        torch.nn.init.uniform_(shard.tensor, a=a, b=b)
    return sharded_tensor

