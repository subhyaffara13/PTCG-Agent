
def scatter(
    x: float | ArrayLike,
    y: float | ArrayLike,
    s: float | ArrayLike | None = None,
    c: ArrayLike | Sequence[ColorType] | ColorType | None = None,
    marker: MarkerType | None = None,
    cmap: str | Colormap | None = None,
    norm: str | Normalize | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    alpha: float | None = None,
    linewidths: float | Sequence[float] | None = None,
    *,
    edgecolors: Literal["face", "none"] | ColorType | Sequence[ColorType] | None = None,
    colorizer: Colorizer | None = None,
    plotnonfinite: bool = False,
    data: DataParamType = None,
    **kwargs,
) -> PathCollection:
    __ret = gca().scatter(
        x,
        y,
        s=s,
        c=c,
        marker=marker,
        cmap=cmap,
        norm=norm,
        vmin=vmin,
        vmax=vmax,
        alpha=alpha,
        linewidths=linewidths,
        edgecolors=edgecolors,
        colorizer=colorizer,
        plotnonfinite=plotnonfinite,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )
    sci(__ret)
    return __ret


def scatter(
    tensor: torch.Tensor,
    scatter_list: list[torch.Tensor] | None = None,
    src: int | None = None,
    group: ProcessGroup | None = None,
    async_op: bool = False,
    group_src: int | None = None,
):
    """
    Scatters a list of tensors to all processes in a group.

    Each process will receive exactly one tensor and store its data in the
    ``tensor`` argument.

    Complex tensors are supported.

    Args:
        tensor (Tensor): Output tensor.
        scatter_list (list[Tensor]): List of tensors to scatter (default is
            None, must be specified on the source rank)
        src (int): Source rank on global process group (regardless of ``group`` argument).
            (If both ``src`` and ``group_src`` are None, default is global rank 0)
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        group_src (int, optional): Source rank on ``group``.  Invalid to specify both ``src`` and ``group_src``

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    .. note:: Note that all Tensors in scatter_list must have the same size.

    Example::
        >>> # xdoctest: +SKIP("need process group init")
        >>> # Note: Process group initialization omitted on each rank.
        >>> import torch.distributed as dist
        >>> tensor_size = 2
        >>> device = torch.device(f'cuda:{rank}')
        >>> output_tensor = torch.zeros(tensor_size, device=device)
        >>> if dist.get_rank() == 0:
        >>>     # Assumes world_size of 2.
        >>>     # Only tensors, all of which must be the same size.
        >>>     t_ones = torch.ones(tensor_size, device=device)
        >>>     t_fives = torch.ones(tensor_size, device=device) * 5
        >>>     scatter_list = [t_ones, t_fives]
        >>> else:
        >>>     scatter_list = None
        >>> dist.scatter(output_tensor, scatter_list, src=0)
        >>> # Rank i gets scatter_list[i].
        >>> output_tensor
        tensor([1., 1.], device='cuda:0') # Rank 0
        tensor([5., 5.], device='cuda:1') # Rank 1

    """
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            scatter,
            relevant_args,
            tensor,
            scatter_list=scatter_list,
            src=src,
            group=group,
            async_op=async_op,
            group_src=group_src,
        )

    _check_single_tensor(tensor, "tensor")
    # Parameter ``scatter_list`` may be left unspecified on non-src ranks.
    if scatter_list:
        _check_tensor_list(scatter_list, "scatter_list")
    else:
        scatter_list = []
    _ensure_all_tensors_same_dtype(tensor, scatter_list)
    group = _group_or_default_group(group)
    if src is None and group_src is None:
        src = 0
    group_src = _canonicalize_group_rank(group, src, group_src, return_global=False)
    if _rank_not_in_group(group):
        _warn_not_in_group("scatter")
        return
    scatter_list = [
        t if not t.is_complex() else torch.view_as_real(t) for t in scatter_list
    ]
    tensor = tensor if not tensor.is_complex() else torch.view_as_real(tensor)

    my_group_rank = group.rank()
    if group_src == my_group_rank:
        if not scatter_list:
            raise ValueError(
                "Argument ``scatter_list`` must be specified on source rank."
            )
        input_tensors = [scatter_list]
        output_tensors = [tensor]
    else:
        if scatter_list:
            raise ValueError(
                "Argument ``scatter_list`` must NOT be specified on non-source ranks."
            )
        input_tensors = []
        output_tensors = [tensor]

    opts = ScatterOptions()
    opts.rootRank = group_src
    opts.asyncOp = async_op
    work = group.scatter(output_tensors, input_tensors, opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def scatter(x, dim: int, index, src, **kwargs):
    return scatter_(clone(x), dim, index, src, **kwargs)


def scatter(g: jit_utils.GraphContext, self, dim, index, src):
    src_type = _type_utils.JitScalarType.from_value(src)
    src = symbolic_helper._maybe_get_scalar(src)
    if symbolic_helper._is_value(src):
        return g.op("ScatterElements", self, index, src, axis_i=dim)
    else:
        # Check if scalar "src" has same type as self (PyTorch allows different
        # type for scalar src (but not when src is tensor)). If not, insert Cast node.
        if _type_utils.JitScalarType.from_value(self) != src_type:
            src = g.op(
                "Cast",
                src,
                to_i=_type_utils.JitScalarType.from_value(self).onnx_type(),
            )
        return g.op(
            "ScatterElements", self, index, opset9.expand_as(g, src, index), axis_i=dim
        )


def scatter(g: jit_utils.GraphContext, self, dim, index, src):
    src_type = _type_utils.JitScalarType.from_value(
        src, _type_utils.JitScalarType.UNDEFINED
    )
    src = symbolic_helper._maybe_get_scalar(src)
    if symbolic_helper._is_value(src):
        return g.op("Scatter", self, index, src, axis_i=dim)
    else:
        # Check if scalar "src" has same type as self (PyTorch allows different
        # type for scalar src (but not when src is tensor)). If not, insert Cast node.
        self_scalar_type = _type_utils.JitScalarType.from_value(self)
        if self_scalar_type != src_type:
            src = g.op("Cast", src, to_i=self_scalar_type.onnx_type())
        return g.op("Scatter", self, index, expand_as(g, src, index), axis_i=dim)


def scatter(tensor, devices=None, chunk_sizes=None, dim=0, streams=None, *, out=None):
    """Scatters tensor across multiple GPUs.

    Args:
        tensor (Tensor): tensor to scatter. Can be on CPU or GPU.
        devices (Iterable[torch.device, str or int], optional): an iterable of
          GPU devices, among which to scatter.
        chunk_sizes (Iterable[int], optional): sizes of chunks to be placed on
          each device. It should match :attr:`devices` in length and sums to
          ``tensor.size(dim)``. If not specified, :attr:`tensor` will be divided
          into equal chunks.
        dim (int, optional): A dimension along which to chunk :attr:`tensor`.
          Default: ``0``.
        streams (Iterable[torch.cuda.Stream], optional): an iterable of Streams, among
          which to execute the scatter. If not specified, the default stream will
          be utilized.
        out (Sequence[Tensor], optional, keyword-only): the GPU tensors to
          store output results. Sizes of these tensors must match that of
          :attr:`tensor`, except for :attr:`dim`, where the total size must
          sum to ``tensor.size(dim)``.

    .. note::
        Exactly one of :attr:`devices` and :attr:`out` must be specified. When
        :attr:`out` is specified, :attr:`chunk_sizes` must not be specified and
        will be inferred from sizes of :attr:`out`.

    Returns:
        - If :attr:`devices` is specified,
            a tuple containing chunks of :attr:`tensor`, placed on
            :attr:`devices`.
        - If :attr:`out` is specified,
            a tuple containing :attr:`out` tensors, each containing a chunk of
            :attr:`tensor`.
    """
    tensor = _handle_complex(tensor)
    if out is None:
        # pyrefly: ignore [not-iterable]
        devices = [_get_device_index(d) for d in devices]
        return tuple(torch._C._scatter(tensor, devices, chunk_sizes, dim, streams))
    else:
        if devices is not None:
            raise RuntimeError(
                f"'devices' must not be specified when 'out' is specified, but got devices={devices}"
            )
        if chunk_sizes is not None:
            raise RuntimeError(
                f"'chunk_sizes' must not be specified when 'out' is specified, but got chunk_sizes={chunk_sizes}"
            )
        return tuple(torch._C._scatter_out(tensor, out, dim, streams))


def scatter(
    inputs: torch.Tensor,
    target_gpus: Sequence[int | torch.device],
    dim: int = ...,
) -> tuple[torch.Tensor, ...]: ...


def scatter(
    inputs: T,
    target_gpus: Sequence[int | torch.device],
    dim: int = ...,
) -> list[T]: ...


def scatter(inputs, target_gpus, dim=0):
    r"""Slice tensors into approximately equal chunks and distributes them across given GPUs.

    Duplicates references to objects that are not tensors.
    """

    def scatter_map(obj):
        if isinstance(obj, torch.Tensor):
            return Scatter.apply(target_gpus, None, dim, obj)
        if _is_namedtuple(obj):
            return [
                type(obj)(*args)
                # pyrefly: ignore [bad-argument-type, no-matching-overload]
                for args in zip(*map(scatter_map, obj), strict=False)
            ]
        if isinstance(obj, tuple) and len(obj) > 0:
            # pyrefly: ignore [bad-argument-type, no-matching-overload]
            return list(zip(*map(scatter_map, obj), strict=False))
        if isinstance(obj, list) and len(obj) > 0:
            # pyrefly: ignore [bad-argument-type, no-matching-overload]
            return [list(i) for i in zip(*map(scatter_map, obj), strict=False)]
        if isinstance(obj, dict) and len(obj) > 0:
            return [
                type(obj)(i)
                # pyrefly: ignore [bad-argument-type, no-matching-overload]
                for i in zip(*map(scatter_map, obj.items()), strict=False)
            ]
        return [obj for _ in target_gpus]

    # After scatter_map is called, a scatter_map cell will exist. This cell
    # has a reference to the actual function scatter_map, which has references
    # to a closure that has a reference to the scatter_map cell (because the
    # fn is recursive). To avoid this reference cycle, we set the function to
    # None, clearing the cell
    try:
        res = scatter_map(inputs)
    finally:
        scatter_map = None  # type: ignore[assignment]
    return res


def scatter(tensors, src=0, group=group.WORLD):
    """
    Scatters a list of tensors to all processes in a group.

    Each process will receive exactly one tensor and store its data in the
    ``tensor`` argument.

    Arguments:
        tensors (list[Tensor]): List of tensors to scatter on the source rank.
            Receivers must pass ``None`.
        src (int, optional): Source rank (default is 0).
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        Tensor: Output tensor from the scatter operation.

    """
    if torch.compiler.is_compiling():
        _not_supported_under_compile("scatter")
    return _Scatter.apply(src, group, *tensors)


def scatter(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], scatter_indices: _ods_ir.Value[_ods_ir.RankedTensorType], updates: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], scatter_dimension_numbers: _Union[_Any, _ods_ir.Attribute], *, indices_are_sorted: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, unique_indices: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ScatterOp]:
  op = ScatterOp(result=result, inputs=inputs, scatter_indices=scatter_indices, updates=updates, scatter_dimension_numbers=scatter_dimension_numbers, indices_are_sorted=indices_are_sorted, unique_indices=unique_indices, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def scatter(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], scatter_indices: _ods_ir.Value[_ods_ir.RankedTensorType], updates: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], scatter_dimension_numbers: _Union[_Any, _ods_ir.Attribute], *, indices_are_sorted: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, unique_indices: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ScatterOp]:
  op = ScatterOp(result=result, inputs=inputs, scatter_indices=scatter_indices, updates=updates, scatter_dimension_numbers=scatter_dimension_numbers, indices_are_sorted=indices_are_sorted, unique_indices=unique_indices, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def scatter(result: _Optional[_ods_ir.Type], base: _ods_ir.Value, offsets: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], indices: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], value_to_store: _ods_ir.Value[_ods_ir.VectorType], *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ScatterOp]:
  op = ScatterOp(result=result, base=base, offsets=offsets, indices=indices, mask=mask, valueToStore=value_to_store, alignment=alignment, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def scatter(
  operand: ArrayLike, scatter_indices: ArrayLike, updates: ArrayLike,
  dimension_numbers: ScatterDimensionNumbers, *,
  indices_are_sorted: bool = False, unique_indices: bool = False,
  mode: str | GatherScatterMode | None = None) -> Array:
  """Scatter-update operator.

  Wraps `XLA's Scatter operator
  <https://www.openxla.org/xla/operation_semantics#scatter>`_, where updates
  replace values from `operand`.

  If multiple updates are performed to the same index of operand, they may be
  applied in any order.

  :func:`scatter` is a low-level operator with complicated semantics, and most
  JAX users will never need to call it directly. Instead, you should prefer using
  :func:`jax.numpy.ndarray.at` for more familiary NumPy-style indexing syntax.

  Args:
    operand: an array to which the scatter should be applied
    scatter_indices: an array that gives the indices in `operand` to which each
      update in `updates` should be applied.
    updates: the updates that should be scattered onto `operand`.
    dimension_numbers: a `lax.ScatterDimensionNumbers` object that describes
      how dimensions of `operand`, `start_indices`, `updates` and the output
      relate.
    indices_are_sorted: whether `scatter_indices` is known to be sorted. If
      true, may improve performance on some backends.
    unique_indices: whether the elements to be updated in ``operand`` are
      guaranteed to not overlap with each other. If true, may improve performance on
      some backends. JAX does not check this promise: if the updated elements
      overlap when ``unique_indices`` is ``True`` the behavior is undefined.
    mode: how to handle indices that are out of bounds: when set to 'clip',
      indices are clamped so that the slice is within bounds, and when
      set to 'fill' or 'drop' out-of-bounds updates are dropped. The behavior
      for out-of-bounds indices when set to 'promise_in_bounds' is
      implementation-defined.

  Returns:
    An array containing the values of `operand` and the scattered updates.

  Examples:
    As mentioned above, you should basically never use :func:`scatter` directly,
    and instead perform scatter-style operations using NumPy-style indexing
    expressions via :attr:`jax.numpy.ndarray.at`.

    Here is and example of updating entries in an array using :attr:`jax.numpy.ndarray.at`,
    which lowers to an XLA Scatter operation:

    >>> x = jnp.ones(5)
    >>> indices = jnp.array([1, 2, 4])
    >>> values = jnp.array([2.0, 3.0, 4.0])

    >>> x.at[indices].set(values)
    Array([1., 2., 3., 1., 4.], dtype=float32)

    This syntax also supports several of the optional arguments to :func:`scatter`,
    for example:

    >>> x.at[indices].set(values, indices_are_sorted=True, mode='promise_in_bounds')
    Array([1., 2., 3., 1., 4.], dtype=float32)

    By comparison, here is the equivalent function call using :func:`scatter` directly,
    which is not something typical users should ever need to do:

    >>> lax.scatter(x, indices[:, None], values,
    ...             dimension_numbers=lax.ScatterDimensionNumbers(
    ...                 update_window_dims=(),
    ...                 inserted_window_dims=(0,),
    ...                 scatter_dims_to_operand_dims=(0,)),
    ...             indices_are_sorted=True,
    ...             mode=lax.GatherScatterMode.PROMISE_IN_BOUNDS)
    Array([1., 2., 3., 1., 4.], dtype=float32)
  """
  operand, scatter_indices, updates = core.auto_insert_reshard(
      operand, scatter_indices, updates)
  return scatter_p.bind(
      operand, scatter_indices, updates, update_jaxpr=None,
      update_consts=(), dimension_numbers=dimension_numbers,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=GatherScatterMode.from_any(mode))

