
def narrow(
    tensor: Tensor,
    dim: int,
    start: int | Tensor,
    length: int | Tensor,
    layout=torch.strided,
) -> Tensor:
    r"""
    Constructs a nested tensor (which might be a view) from :attr:`tensor`, a strided tensor. This follows
    similar semantics to torch.Tensor.narrow, where in the :attr:`dim`-th dimension the new nested tensor
    shows only the elements in the interval `[start, start+length)`. As nested representations
    allow for a different `start` and `length` at each 'row' of that dimension, :attr:`start` and :attr:`length`
    can also be tensors of shape `tensor.shape[0]`.

    There's some differences depending on the layout you use for the nested tensor. If using strided layout,
    torch.narrow will do a copy of the narrowed data into a contiguous NT with strided layout, while
    jagged layout narrow() will create a non-contiguous view of your original strided tensor. This particular
    representation is really useful for representing kv-caches in Transformer models, as specialized
    SDPA kernels can deal with format easily, resulting in performance improvements.


    Args:
        tensor (:class:`torch.Tensor`): a strided tensor, which will be used as the underlying data
            for the nested tensor if using the jagged layout or will be copied for the strided layout.
        dim (int): the dimension where narrow will be applied. Only `dim=1` is supported for the
            jagged layout, while strided supports all dim
        start (Union[int, :class:`torch.Tensor`]): starting element for the narrow operation
        length (Union[int, :class:`torch.Tensor`]): number of elements taken during the narrow op

    Keyword arguments:
        layout (:class:`torch.layout`, optional): the desired layout of returned nested tensor.
            Only strided and jagged layouts are supported. Default: if None, the strided layout.

    Example::

        >>> starts = torch.tensor([0, 1, 2, 3, 4], dtype=torch.int64)
        >>> lengths = torch.tensor([3, 2, 2, 1, 5], dtype=torch.int64)
        >>> narrow_base = torch.randn(5, 10, 20)
        >>> nt_narrowed = torch.nested.narrow(narrow_base, 1, starts, lengths, layout=torch.jagged)
        >>> nt_narrowed.is_contiguous()
        False
    """
    if not isinstance(start, (int, SymInt, Tensor)):
        raise RuntimeError("start must be an integer or a tensor")

    if not isinstance(length, (int, SymInt, Tensor)):
        raise RuntimeError("length must be an integer or a tensor")

    if layout == torch.strided:
        if isinstance(start, Tensor) or isinstance(length, Tensor):
            raise RuntimeError(
                "start and length must be integers for the strided layout NT impl"
            )
        # TODO: switch to as_nested_tensor(tensor) when it is available
        nt = as_nested_tensor(torch.unbind(tensor), layout=torch.strided).narrow(
            dim, start, length
        )
    elif layout == torch.jagged:
        if dim != 1:
            raise RuntimeError("jagged layout only supports dim=1")

        from torch.nested._internal.nested_tensor import jagged_from_tensor_and_lengths

        if isinstance(start, (int, SymInt)):
            start = torch.tensor([start], device=tensor.device, dtype=torch.int64)

        if isinstance(length, (int, SymInt)):
            length = torch.tensor([length], device=tensor.device, dtype=torch.int64)

        nt, _, _ = jagged_from_tensor_and_lengths(tensor, start, length)
    else:
        raise RuntimeError(
            f"Specified layout is unsupported for nested narrow: {layout}"
        )

    return nt


def narrow(
    a: TensorLikeType, dim: int, start: int | TensorLikeType, length: int
) -> TensorLikeType:
    # Supports Tensor overload that was added for XLA:
    # https://github.com/pytorch/pytorch/issues/31558
    if isinstance(start, TensorLike):
        torch._check(
            start.dim() == 0 and utils.is_integer_dtype(start.dtype),
            lambda: "start must be an 0-dim integral Tensor.",
        )
        start = start.item()  # type: ignore[assignment]
    start = cast(int, start)
    torch._check(a.dim() > 0, lambda: "narrow() cannot be applied to a 0-dim tensor.")
    torch._check(length >= 0, lambda: "narrow(): length must be non-negative.")
    dim = utils.canonicalize_dim(a.ndim, dim)
    dim_length = a.size(dim)
    torch._check_with(
        IndexError,
        -dim_length <= start and start <= dim_length,
        lambda: f"start out of range (expected to be in range of [{-dim_length}, {dim_length}], but got {start})",
    )
    if start < 0:
        start = start + dim_length
    torch._check(
        start <= dim_length - length,
        lambda: f"start ({start}) + length ({length}) exceeds dimension size ({dim_length}).",
    )
    new_shape = list(a.shape)
    new_shape[dim] = length
    return a.as_strided(
        new_shape, a.stride(), a.storage_offset() + a.stride(dim) * start
    )


def narrow(g: jit_utils.GraphContext, input, dim, start, length):
    end = g.op("Add", start, length)
    return symbolic_helper._slice_helper(g, input, axes=dim, starts=start, ends=end)


def narrow(g: jit_utils.GraphContext, input, dim, start, length):
    return symbolic_helper._slice_helper(
        g, input, axes=[dim], starts=[start], ends=[start + length]
    )


def narrow(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    inp = new_kwargs.pop("input")

    dim = _wrap_jagged_dim(inp.dim(), new_kwargs["dim"], inp._ragged_idx, "narrow")
    values = func(
        inp._values,
        dim=dim,
        start=new_kwargs["start"],
        length=new_kwargs["length"],
    )
    return NestedTensor(values, **extract_kwargs(inp))

