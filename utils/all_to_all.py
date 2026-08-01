
def all_to_all(
    output_tensor_list, input_tensor_list, group=None, async_op: bool = False
):
    """
    Scatters list of input tensors to all processes in a group and return gathered list of tensors in output list.

    Complex tensors are supported.

    Args:
        output_tensor_list (list[Tensor]): List of tensors to be gathered one
            per rank.
        input_tensor_list (list[Tensor]): List of tensors to scatter one per rank.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group.

    .. warning::
        `all_to_all` is experimental and subject to change.

    Examples:
        >>> # xdoctest: +SKIP("Undefined rank")
        >>> input = torch.arange(4) + rank * 4
        >>> input = list(input.chunk(4))
        >>> input
        [tensor([0]), tensor([1]), tensor([2]), tensor([3])]     # Rank 0
        [tensor([4]), tensor([5]), tensor([6]), tensor([7])]     # Rank 1
        [tensor([8]), tensor([9]), tensor([10]), tensor([11])]   # Rank 2
        [tensor([12]), tensor([13]), tensor([14]), tensor([15])] # Rank 3
        >>> output = list(torch.empty([4], dtype=torch.int64).chunk(4))
        >>> dist.all_to_all(output, input)
        >>> output
        [tensor([0]), tensor([4]), tensor([8]), tensor([12])]    # Rank 0
        [tensor([1]), tensor([5]), tensor([9]), tensor([13])]    # Rank 1
        [tensor([2]), tensor([6]), tensor([10]), tensor([14])]   # Rank 2
        [tensor([3]), tensor([7]), tensor([11]), tensor([15])]   # Rank 3

        >>> # Essentially, it is similar to following operation:
        >>> scatter_list = input
        >>> gather_list = output
        >>> for i in range(world_size):
        >>>     dist.scatter(gather_list[i], scatter_list if i == rank else [], src=i)

        >>> input
        tensor([0, 1, 2, 3, 4, 5])                                       # Rank 0
        tensor([10, 11, 12, 13, 14, 15, 16, 17, 18])                     # Rank 1
        tensor([20, 21, 22, 23, 24])                                     # Rank 2
        tensor([30, 31, 32, 33, 34, 35, 36])                             # Rank 3
        >>> input_splits
        [2, 2, 1, 1]                                                     # Rank 0
        [3, 2, 2, 2]                                                     # Rank 1
        [2, 1, 1, 1]                                                     # Rank 2
        [2, 2, 2, 1]                                                     # Rank 3
        >>> output_splits
        [2, 3, 2, 2]                                                     # Rank 0
        [2, 2, 1, 2]                                                     # Rank 1
        [1, 2, 1, 2]                                                     # Rank 2
        [1, 2, 1, 1]                                                     # Rank 3
        >>> input = list(input.split(input_splits))
        >>> input
        [tensor([0, 1]), tensor([2, 3]), tensor([4]), tensor([5])]                   # Rank 0
        [tensor([10, 11, 12]), tensor([13, 14]), tensor([15, 16]), tensor([17, 18])] # Rank 1
        [tensor([20, 21]), tensor([22]), tensor([23]), tensor([24])]                 # Rank 2
        [tensor([30, 31]), tensor([32, 33]), tensor([34, 35]), tensor([36])]         # Rank 3
        >>> output = ...
        >>> dist.all_to_all(output, input)
        >>> output
        [tensor([0, 1]), tensor([10, 11, 12]), tensor([20, 21]), tensor([30, 31])]   # Rank 0
        [tensor([2, 3]), tensor([13, 14]), tensor([22]), tensor([32, 33])]           # Rank 1
        [tensor([4]), tensor([15, 16]), tensor([23]), tensor([34, 35])]              # Rank 2
        [tensor([5]), tensor([17, 18]), tensor([24]), tensor([36])]                  # Rank 3

        >>> # Another example with tensors of torch.cfloat type.
        >>> input = torch.tensor(
        ...     [1 + 1j, 2 + 2j, 3 + 3j, 4 + 4j], dtype=torch.cfloat
        ... ) + 4 * rank * (1 + 1j)
        >>> input = list(input.chunk(4))
        >>> input
        [tensor([1+1j]), tensor([2+2j]), tensor([3+3j]), tensor([4+4j])]            # Rank 0
        [tensor([5+5j]), tensor([6+6j]), tensor([7+7j]), tensor([8+8j])]            # Rank 1
        [tensor([9+9j]), tensor([10+10j]), tensor([11+11j]), tensor([12+12j])]      # Rank 2
        [tensor([13+13j]), tensor([14+14j]), tensor([15+15j]), tensor([16+16j])]    # Rank 3
        >>> output = list(torch.empty([4], dtype=torch.int64).chunk(4))
        >>> dist.all_to_all(output, input)
        >>> output
        [tensor([1+1j]), tensor([5+5j]), tensor([9+9j]), tensor([13+13j])]          # Rank 0
        [tensor([2+2j]), tensor([6+6j]), tensor([10+10j]), tensor([14+14j])]        # Rank 1
        [tensor([3+3j]), tensor([7+7j]), tensor([11+11j]), tensor([15+15j])]        # Rank 2
        [tensor([4+4j]), tensor([8+8j]), tensor([12+12j]), tensor([16+16j])]        # Rank 3

    """
    relevant_args = (
        tuple(input_tensor_list)
        if isinstance(input_tensor_list, (list, tuple))
        else (input_tensor_list,)
    )
    if has_torch_function(relevant_args):
        return handle_torch_function(
            all_to_all,
            relevant_args,
            output_tensor_list,
            input_tensor_list,
            group=group,
            async_op=async_op,
        )

    if _rank_not_in_group(group):
        _warn_not_in_group("all_to_all")
        return

    opts = AllToAllOptions()
    opts.asyncOp = async_op
    _check_tensor_list(output_tensor_list, "output_tensor_list")
    _check_tensor_list(input_tensor_list, "input_tensor_list")
    _ensure_all_tensors_same_dtype(output_tensor_list, input_tensor_list)

    input_tensor_list = [
        t if not t.is_complex() else torch.view_as_real(t) for t in input_tensor_list
    ]
    output_tensor_list = [
        t if not t.is_complex() else torch.view_as_real(t) for t in output_tensor_list
    ]

    group = group or _get_default_group()
    work = group.alltoall(output_tensor_list, input_tensor_list, opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def all_to_all(output_tensor_list, input_tensor_list, group=group.WORLD):
    """
    Each process scatters list of input tensors to all processes in a group and return gathered list of tensors in output list.

    Arguments:
        output_tensor_list (list[Tensor]): list of tensors to gather one per rank.
        input_tensor_list (list[Tensor]): List of tensors to scatter one per rank.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        tuple([Tensor]): Output of the collective.

    """
    if torch.compiler.is_compiling():
        _not_supported_under_compile("all_to_all")
    return _AlltoAll.apply(group, output_tensor_list, *input_tensor_list)


def all_to_all(operand: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], replica_groups: _Union[_Any, _ods_ir.Attribute], *, split_dimension: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, concat_dimension: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, split_count: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, AllToAllOp]:
  op = AllToAllOp(operand=operand, replica_groups=replica_groups, split_dimension=split_dimension, concat_dimension=concat_dimension, split_count=split_count, channel_handle=channel_handle, results=results, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def all_to_all(tensor: _ods_ir.Value, params: _Union[_Any, _ods_ir.Attribute], out_sharding: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AllToAllOp(tensor=tensor, params=params, out_sharding=out_sharding, results=results, loc=loc, ip=ip).result


def all_to_all(operands_: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], split_dimension: _Union[int, _ods_ir.IntegerAttr], concat_dimension: _Union[int, _ods_ir.IntegerAttr], split_count: _Union[int, _ods_ir.IntegerAttr], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, AllToAllOp]:
  op = AllToAllOp(operands_=operands_, split_dimension=split_dimension, concat_dimension=concat_dimension, split_count=split_count, replica_groups=replica_groups, channel_handle=channel_handle, results=results, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def all_to_all(x, axis_name, split_axis, concat_axis, *, axis_index_groups=None,
               tiled=False):
  """Materialize the mapped axis and map a different axis.

  If ``x`` is a pytree then the result is equivalent to mapping this function to
  each leaf in the tree.

  In the output, the input mapped axis ``axis_name`` is materialized at the
  logical axis position ``concat_axis``, and the input unmapped axis at position
  ``split_axis`` is mapped with the name ``axis_name``.

  The group size of the mapped axis size must be equal to the size of the
  unmapped axis; that is, we must have
  ``lax.psum(1, axis_name, axis_index_groups=axis_index_groups) == x.shape[axis]``.
  By default, when ``axis_index_groups=None``, this encompasses all the devices.

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a pmapped axis (see the
      :func:`jax.pmap` documentation for more details).
    split_axis: int indicating the unmapped axis of ``x`` to map with the name
      ``axis_name``.
    concat_axis: int indicating the position in the output to materialize the
      mapped axis of the input with the name ``axis_name``.
    axis_index_groups: optional list of lists containing axis indices (e.g. for
      an axis of size 4, [[0, 1], [2, 3]] would run all_to_all over the first
      two and last two replicas). Groups must cover all axis indices exactly
      once, and all groups must be the same size.
    tiled: when True, all_to_all will divide split_axis into chunks and concatenate
      them along concat_axis. In particular, no dimensions are added or removed.
      False by default.

  Returns:
    When tiled is False, array(s) with shape given by the expression::

      np.insert(np.delete(x.shape, split_axis), concat_axis, axis_size)

    where ``axis_size`` is the size of the mapped axis named ``axis_name`` in
    the input ``x``.

    Otherwise array with shape similar to the input shape, except with split_axis
    divided by axis size and concat_axis multiplied by axis size.
  """
  return _all_to_all_is_async(x, axis_name, split_axis, concat_axis,
                              axis_index_groups=axis_index_groups, tiled=tiled,
                              is_async=False)

