from typing import Any, Callable

def reduce(
    inputs: Sequence[torch.Tensor],
    output: torch.Tensor | Sequence[torch.Tensor] | None = None,
    root: int = 0,
    op: int = SUM,
    streams: Sequence[torch.cuda.Stream] | None = None,
    comms=None,
    *,
    outputs: Sequence[torch.Tensor] | None = None,
) -> None:
    _check_sequence_type(inputs)
    _output: torch.Tensor
    if outputs is not None:
        if output is not None:
            raise ValueError(
                "'output' and 'outputs' can not be both specified. 'outputs' is deprecated in "
                "favor of 'output', taking in a single output tensor. The signature of reduce is: "
                "reduce(inputs, output=None, root=0, op=SUM, streams=None, comms=None)."
            )
        else:
            warnings.warn(
                "`nccl.reduce` with an output tensor list is deprecated. "
                "Please specify a single output tensor with argument 'output' instead instead.",
                FutureWarning,
                stacklevel=2,
            )
            _output = outputs[root]
    elif not isinstance(output, torch.Tensor) and isinstance(
        output, collections.abc.Sequence
    ):
        # User called old API with positional arguments of list of output tensors.
        warnings.warn(
            "nccl.reduce with an output tensor list is deprecated. "
            "Please specify a single output tensor.",
            FutureWarning,
            stacklevel=2,
        )
        _output = output[root]
    else:
        _output = inputs[root] if output is None else output
    torch._C._nccl_reduce(inputs, _output, root, op, streams, comms)


def reduce(
    tensor: torch.Tensor,
    dst: int | None = None,
    op=ReduceOp.SUM,
    group: ProcessGroup | None = None,
    async_op: bool = False,
    group_dst: int | None = None,
):
    """
    Reduces the tensor data across all machines.

    Only the process with rank ``dst`` is going to receive the final result.

    Args:
        tensor (Tensor): Input and output of the collective. The function
            operates in-place.
        dst (int): Destination rank on global process group (regardless of ``group`` argument)
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        group_dst (int): Destination rank on ``group``.  Must specify one of ``group_dst``
            and ``dst`` but not both.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    """
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            reduce,
            relevant_args,
            tensor,
            dst=dst,
            op=op,
            group=group,
            async_op=async_op,
            group_dst=group_dst,
        )

    group = _group_or_default_group(group)
    group_dst = _canonicalize_group_rank(group, dst, group_dst, return_global=False)
    _check_single_tensor(tensor, "tensor")
    if _rank_not_in_group(group):
        _warn_not_in_group("reduce")
        return

    opts = ReduceOptions()
    opts.reduceOp = op
    opts.rootRank = group_dst
    opts.asyncOp = async_op
    work = group.reduce([tensor], opts)
    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def reduce(
    function: Callable[[_U, _T], _U],
    iterable: Iterable[_T],
    initial: _U = _initial_missing,  # type: ignore[assignment]
    /,
) -> _U:
    it = iter(iterable)

    value: _U
    if initial is _initial_missing:
        try:
            value = next(it)  # type: ignore[assignment]
        except StopIteration:
            raise TypeError(
                "reduce() of empty iterable with no initial value",
            ) from None
    else:
        value = initial

    for element in it:
        value = function(value, element)

    return value


def reduce(tensor, dst, op=ReduceOp.SUM, group=group.WORLD):
    """
    Reduces the tensor data across all machines.

    Only the process with rank ``dst`` is going to receive the final result.

    Arguments:
        tensor (Tensor): Input of the collective.
        dst (int): Destination rank.
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        Tensor: Output of the collective.

    """
    if torch.compiler.is_compiling():
        _not_supported_under_compile("reduce")
    return _Reduce.apply(dst, op, group, tensor)


def reduce(
    quat: Array,
    left: Array | None = None,
    right: Array | None = None,
) -> tuple[Array, Array | None, Array | None]:
    if left is None and right is None:
        return quat, None, None
    # DECISION: We cannot have variable number of return arguments for jit compiled
    # functions. We therefore always return the indices, and filter out later.
    # TOOD: Properly support broadcasting.
    xp = array_namespace(quat)
    quat = xpx.atleast_nd(quat, ndim=2, xp=xp)
    if left is None:
        left = xp.ones_like(quat)
    if right is None:
        right = xp.ones_like(quat)

    # We want to calculate the real components of q = l * p * r. It can
    # be shown that:
    #     qs = ls * ps * rs - ls * dot(pv, rv) - ps * dot(lv, rv)
    #          - rs * dot(lv, pv) - dot(cross(lv, pv), rv)
    # where ls and lv denote the scalar and vector components of l.

    p = quat
    ps, pv = _split_rotation(p, xp)
    ls, lv = _split_rotation(left, xp)
    rs, rv = _split_rotation(right, xp)

    # Compute each term without einsum (not accessible in the Array API)
    # First term: np.einsum("i,j,k", ls, ps, rs)
    term1 = ls[..., :, None, None] * ps[..., None, :, None] * rs[..., None, None, :]
    # Second term: np.einsum('i,jx,kx', ls, pv, rv)
    prv = xp.sum(pv[..., :, None, :] * rv[..., None, :, :], axis=-1)
    term2 = ls[..., :, None, None] * prv[..., None, :, :]
    # Third term: np.einsum('ix,j,kx', lv, ps, rv)
    lrv = xp.sum(lv[..., :, None, :] * rv[..., None, :, :], axis=-1)
    term3 = ps[..., None, :, None] * lrv[..., :, None, :]
    # Fourth term: np.einsum('ix,jx,k', lv, pv, rs)
    lpv = xp.sum(lv[..., :, None, :] * pv[..., None, :, :], axis=-1)
    term4 = rs[..., None, None, :] * lpv[..., :, :, None]
    # Fifth term: np.einsum('xyz,ix,jy,kz', e, lv, pv, rv). We want to avoid expanding
    # the einsum into a 6D tensor to avoid excessive memory usage. Instead, we compute
    # the cross product between lv and pv and then compute the dot product with rv.
    # First compute cross products between lv and pv
    lv_expanded = lv[..., :, None, :]
    pv_expanded = pv[..., None, :, :]
    cross_lp = xp.linalg.cross(lv_expanded, pv_expanded)
    # Then compute dot product with rv
    term5 = xp.sum(cross_lp[..., :, :, None, :] * rv[..., None, None, :, :], axis=-1)
    # Combine all terms with proper shape alignment
    qs = xp.abs(term1 - term2 - term3 - term4 - term5)
    qs = xp.reshape(xp.moveaxis(qs, 1, 0), (qs.shape[1], -1))

    # Find best indices from scalar components
    max_ind = xp.argmax(xp.reshape(qs, (qs.shape[0], -1)), axis=1)
    left_best = max_ind // rv.shape[0]
    right_best = max_ind % rv.shape[0]
    # Array API limitation: Integer index arrays are only allowed with integer indices
    # TODO: Can we somehow avoid this?
    all_idx = xp.reshape(xp.arange(left.shape[-1]), (1, -1))
    left_idx = xp.reshape(left_best, (-1, 1))
    left = left[left_idx, all_idx]
    right_idx = xp.reshape(right_best, (-1, 1))
    right = right[right_idx, all_idx]

    # Reduce the rotation using the best indices
    reduced = compose_quat(left, compose_quat(p, right))

    if left is None:
        left_best = None
    if right is None:
        right_best = None
    return reduced, left_best, right_best


def reduce(result: _Sequence[_ods_ir.Type], srcs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], axis: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ReduceOp]:
  op = ReduceOp(result=result, srcs=srcs, axis=axis, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def reduce(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], init_values: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], dimensions: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ReduceOp]:
  op = ReduceOp(result=result, inputs=inputs, init_values=init_values, dimensions=dimensions, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def reduce(tensors: _Sequence[_ods_ir.Value], *, reduction: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ReduceOp(tensors=tensors, reduction=reduction, results=results, loc=loc, ip=ip).result


def reduce(operands_: _Sequence[_ods_ir.Value], num_reductions: int, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ReduceOp:
  return ReduceOp(operands_=operands_, num_reductions=num_reductions, loc=loc, ip=ip)


def reduce(x: _ods_ir.Value, y: _ods_ir.Value, identity: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ReduceOp(x=x, y=y, identity=identity, results=results, loc=loc, ip=ip).result


def reduce(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], init_values: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], dimensions: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ReduceOp]:
  op = ReduceOp(result=result, inputs=inputs, init_values=init_values, dimensions=dimensions, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def reduce(operand, init_value, computation, dimensions):
  reducer = _make_reducer(computation, init_value)
  return reducer(operand, tuple(dimensions)).astype(np.asarray(operand).dtype)


def reduce(function: Callable[[T, Any], T],
           tree: Any,
           initializer: T | tree_util.Unspecified = tree_util.Unspecified(),
           is_leaf: Callable[[Any], bool] | None = None) -> T:
  """Call reduce() over the leaves of a tree.

  Args:
    function: the reduction function
    tree: the pytree to reduce over
    initializer: the optional initial value
    is_leaf : an optionally specified function that will be called at each
      flattening step. It should return a boolean, which indicates whether the
      flattening should traverse the current object, or if it should be stopped
      immediately, with the whole subtree being treated as a leaf.

  Returns:
    result: the reduced value.

  Examples:
    >>> import jax
    >>> import operator
    >>> jax.tree.reduce(operator.add, [1, (2, 3), [4, 5, 6]])
    21

  Notes:
    **Tip**: You can exclude leaves from the reduction by first mapping them to
    ``None`` using :func:`jax.tree.map`. This causes them to not be counted as
    leaves after that.

  See Also:
    - :func:`jax.tree.reduce_associative`
    - :func:`jax.tree.leaves`
    - :func:`jax.tree.map`
  """
  return tree_util.tree_reduce(function, tree, initializer, is_leaf=is_leaf)


def reduce(operands: Any,
           init_values: Any,
           computation: Callable[[Any, Any], Any],
           dimensions: Sequence[int],
           out_sharding: NamedSharding | P | None = None) -> Any:
  """Wraps XLA's `Reduce
  <https://www.openxla.org/xla/operation_semantics#reduce>`_
  operator.

  ``init_values`` and ``computation`` together must form a `monoid
  <https://en.wikipedia.org/wiki/Monoid>`_
  for correctness. That is ``init_values`` must be an identity of
  ``computation``, and ``computation`` must be associative. XLA may exploit both
  of these properties during code generation; if either is violated the result
  is undefined.

  ``init_values`` must consist of scalars.
  """
  flat_operands, operand_tree = tree_util.tree_flatten(operands)
  comp_debug = api_util.debug_info("reduce comp", computation,
                                   (init_values, init_values), {})
  flat_init_values, init_value_tree = tree_util.tree_flatten(init_values)
  if operand_tree != init_value_tree:
    raise ValueError('Operands must have the same tree structure as init_values:'
                     f' {operand_tree} vs. {init_value_tree}')
  if len(flat_operands) != len(flat_init_values):
    raise ValueError('Must have same total number of operands as init_values: '
                     f' {len(flat_operands)} vs. {len(flat_init_values)}')
  monoid_reducer = _get_monoid_reducer(computation, flat_init_values)
  if monoid_reducer:
    # monoid reducers bypass the weak_type_rule, so we set it explicitly.
    weak_type = (dtypes.is_weakly_typed(*flat_operands) and
                 dtypes.is_weakly_typed(*flat_init_values))
    if out_sharding is not None and monoid_reducer is not reduce_sum:
      raise NotImplementedError
    out_sharding_dict = ({'out_sharding': out_sharding}
                         if out_sharding is not None else {})
    out = monoid_reducer(*flat_operands, dimensions, **out_sharding_dict)
    return _convert_element_type(out, weak_type=weak_type)
  else:
    flat_init_avals = safe_map(core.typeof, flat_init_values)
    closed_jaxpr, out_tree = _variadic_reduction_jaxpr(
        computation, comp_debug, tuple(flat_init_avals), init_value_tree)
    flat_operands = core.auto_insert_reshard(*flat_operands)
    flat_init_values = core.auto_insert_reshard(*flat_init_values)
    out = reduce_p.bind(*flat_operands, *flat_init_values, computation=computation,
                        jaxpr=closed_jaxpr, dimensions=tuple(dimensions))
    return tree_util.tree_unflatten(out_tree, out)


def reduce(
    constraint_system: ConstraintSystem,
) -> ConstraintSystem | Unsatisfiable:
  """Reduces a constraint system until it can no longer be reduced.

  Returns:
    - Unsatisfiable(): if the constraint system is unsatisfiable.
    - The maximally reduced constraint system otherwise.
  """
  while True:
    match _reduce_system_once(constraint_system):
      case None:
        break
      case Unsatisfiable():
        return Unsatisfiable()
      case ConstraintSystem() as new_system:
        constraint_system = new_system
      case _ as never:
        assert_never(never)  # pyrefly: ignore[bad-argument-type]  # pyrefly#2858

  return constraint_system

