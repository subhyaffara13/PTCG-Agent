
def select(self: list[int], dim: int, index: int):
    ndim = len(self)
    if ndim == 0:
        raise AssertionError("Cannot select from a 0-dimensional tensor")
    dim = maybe_wrap_dim(dim, ndim)
    size = self[dim]
    if index < -size or index >= size:
        raise AssertionError(
            f"Index {index} is out of bounds for dimension {dim} with size {size}"
        )
    if index < 0:
        index += size
    out: list[int] = []
    for i in range(ndim):
        if i != dim:
            out.append(self[i])
    return out


def select(x, dim, idx):
    idx = sympy.expand(idx)
    size = sympy.expand(x.get_size()[dim])
    actual_index = None

    if V.graph.sizevars.guard_or_false(sympy.Lt(idx, 0)):
        actual_index = idx + size
    elif V.graph.sizevars.guard_or_false(sympy.Ge(idx, 0)):
        actual_index = idx

    if actual_index is not None:
        if has_free_unbacked_symbols(idx):
            # Inductor could generate incorrect views for tensors with unbacked symbols here;
            # Squeeze operations are translated to views, resulting in incorrect strides.
            # Additionally, we want to avoid accidental unbacked unsqueeze semantics. To resolve this,
            # we use as_strided instead.
            # Removing this branch will cause test_unbacked_select_index_with_check to fail.

            # before accessing size, stride, and offset we need to realize.
            x.realize()
            new_size = x.get_size()
            new_stride = x.get_stride()
            new_storage_offset = x.get_layout().offset + new_stride[dim] * actual_index

            del new_size[dim]
            del new_stride[dim]
            return as_strided(x, new_size, new_stride, new_storage_offset)
        else:
            # no need to clamp, this function handles negative indexing itself
            slice_result = slice_(x, dim, actual_index, actual_index + 1, clamp=False)
            return squeeze(slice_result, dim)

    # Unbacked Semantics:
    # When the index idx is unbacked (e.g., u0), we compute the index dynamically
    # during the lowering of the select operation using DynamicSelectStorageOffset.

    unbacked_bindings = resolve_unbacked_bindings(
        V.graph.sizevars.shape_env, V.graph.current_node.meta["unbacked_bindings"]
    )
    assert unbacked_bindings is not None
    assert len(unbacked_bindings) == 1, unbacked_bindings
    unbacked_offset_sym, _ = next(iter(unbacked_bindings.items()))

    # before accessing size, stride, and offset we need to realize.
    x.realize()
    new_size = x.get_size()
    new_stride = x.get_stride()
    new_storage_offset = unbacked_offset_sym
    buffer = ir.DynamicSelectStorageOffset(
        unbacked_offset_sym,
        idx,
        x.get_layout().offset,
        new_stride[dim],
        x.get_size()[dim],
        clamp=False,
    )
    buffer.name = V.graph.register_buffer(buffer)
    V.graph.register_operation(buffer)

    del new_size[dim]
    del new_stride[dim]
    return as_strided(x, new_size, new_stride, new_storage_offset)


def select(g: jit_utils.GraphContext, self, dim, index):
    return g.op("Gather", self, index, axis_i=dim)


def select(g: jit_utils.GraphContext, self, dim, index):
    """Implement the select functionality for a pytorch tensor in ONNX.

    Selects elements from the input tensor along the specified `dim` dimension based on the `index` tensor.
    """
    index = symbolic_helper._maybe_get_scalar(index)
    if (not symbolic_helper._is_value(index)) and (index < 0):
        if index == -1:
            end_index = _constants.INT64_MAX
        else:
            end_index = index + 1
        slice_node = symbolic_helper._slice_helper(
            g, self, axes=[dim], starts=[index], ends=[end_index]
        )
        return symbolic_helper._squeeze_helper(g, slice_node, [dim])
    else:
        # FIXME(justinchuby): can index be an int and not a value?
        return g.op("Gather", self, index, axis_i=dim)


def select(data, keys):
  return [subselect(row, keys) for row in data]


def select(condlist, choicelist, default=0):
    """
    Return an array drawn from elements in choicelist, depending on conditions.

    Parameters
    ----------
    condlist : list of bool ndarrays
        The list of conditions which determine from which array in `choicelist`
        the output elements are taken. When multiple conditions are satisfied,
        the first one encountered in `condlist` is used.
    choicelist : list of ndarrays
        The list of arrays from which the output elements are taken. It has
        to be of the same length as `condlist`.
    default : array_like, optional
        The element inserted in `output` when all conditions evaluate to False.

    Returns
    -------
    output : ndarray
        The output at position m is the m-th element of the array in
        `choicelist` where the m-th element of the corresponding array in
        `condlist` is True.

    See Also
    --------
    where : Return elements from one of two arrays depending on condition.
    take, choose, compress, diag, diagonal

    Examples
    --------
    >>> import numpy as np

    Beginning with an array of integers from 0 to 5 (inclusive),
    elements less than ``3`` are negated, elements greater than ``3``
    are squared, and elements not meeting either of these conditions
    (exactly ``3``) are replaced with a `default` value of ``42``.

    >>> x = np.arange(6)
    >>> condlist = [x<3, x>3]
    >>> choicelist = [-x, x**2]
    >>> np.select(condlist, choicelist, 42)
    array([ 0,  -1,  -2, 42, 16, 25])

    When multiple conditions are satisfied, the first one encountered in
    `condlist` is used.

    >>> condlist = [x<=4, x>3]
    >>> choicelist = [x, x**2]
    >>> np.select(condlist, choicelist, 55)
    array([ 0,  1,  2,  3,  4, 25])

    """
    # Check the size of condlist and choicelist are the same, or abort.
    if len(condlist) != len(choicelist):
        raise ValueError(
            'list of cases must be same length as list of conditions')

    # Now that the dtype is known, handle the deprecated select([], []) case
    if len(condlist) == 0:
        raise ValueError("select with an empty condition list is not possible")

    # TODO: This preserves the Python int, float, complex manually to get the
    #       right `result_type` with NEP 50.  Most likely we will grow a better
    #       way to spell this (and this can be replaced).
    choicelist = [
        choice if type(choice) in (int, float, complex) else np.asarray(choice)
        for choice in choicelist]
    choicelist.append(default if type(default) in (int, float, complex)
                      else np.asarray(default))

    try:
        dtype = np.result_type(*choicelist)
    except TypeError as e:
        msg = f'Choicelist and default value do not have a common dtype: {e}'
        raise TypeError(msg) from None

    # Convert conditions to arrays and broadcast conditions and choices
    # as the shape is needed for the result. Doing it separately optimizes
    # for example when all choices are scalars.
    condlist = np.broadcast_arrays(*condlist)
    choicelist = np.broadcast_arrays(*choicelist)

    # If cond array is not an ndarray in boolean format or scalar bool, abort.
    for i, cond in enumerate(condlist):
        if cond.dtype.type is not np.bool:
            raise TypeError(
                f'invalid entry {i} in condlist: should be boolean ndarray')

    if choicelist[0].ndim == 0:
        # This may be common, so avoid the call.
        result_shape = condlist[0].shape
    else:
        result_shape = np.broadcast_arrays(condlist[0], choicelist[0])[0].shape

    result = np.full(result_shape, choicelist[-1], dtype)

    # Use np.copyto to burn each choicelist array onto result, using the
    # corresponding condlist as a boolean mask. This is done in reverse
    # order since the first choice should take precedence.
    choicelist = choicelist[-2::-1]
    condlist = condlist[::-1]
    for choice, cond in zip(choicelist, condlist):
        np.copyto(result, choice, where=cond)

    return result


def select(condition: _ods_ir.Value, true_value: _ods_ir.Value, false_value: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SelectOp(condition=condition, true_value=true_value, false_value=false_value, results=results, loc=loc, ip=ip).result


def select(condition: _ods_ir.Value, true_value: _ods_ir.Value, false_value: _ods_ir.Value, *, fastmath_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SelectOp(condition=condition, trueValue=true_value, falseValue=false_value, fastmathFlags=fastmath_flags, results=results, loc=loc, ip=ip).result


def select(pred: _ods_ir.Value[_ods_ir.RankedTensorType], on_true: _ods_ir.Value[_ods_ir.RankedTensorType], on_false: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SelectOp(pred=pred, on_true=on_true, on_false=on_false, results=results, loc=loc, ip=ip).result


def select(x: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SelectOp(x=x, results=results, loc=loc, ip=ip).result


def select(pred: _ods_ir.Value[_ods_ir.RankedTensorType], on_true: _ods_ir.Value[_ods_ir.RankedTensorType], on_false: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SelectOp(pred=pred, on_true=on_true, on_false=on_false, results=results, loc=loc, ip=ip).result


def select(pred: ArrayLike, on_true: ArrayLike, on_false: ArrayLike) -> Array:
  """Selects between two branches based on a boolean predicate.

  Wraps XLA's `Select
  <https://www.openxla.org/xla/operation_semantics#select>`_
  operator.

  In general :func:`~jax.lax.select` leads to evaluation of both branches, although
  the compiler may elide computations if possible. For a similar function that
  usually evaluates only a single branch, see :func:`~jax.lax.cond`.

  Args:
    pred: boolean array
    on_true: array containing entries to return where ``pred`` is True. Must have
      the same shape as ``pred``, and the same shape and dtype as ``on_false``.
    on_false: array containing entries to return where ``pred`` is False. Must have
      the same shape as ``pred``, and the same shape and dtype as ``on_true``.

  Returns:
    result: array with same shape and dtype as ``on_true`` and ``on_false``.
  """
  # Caution! The select_n_p primitive has the *opposite* order of arguments to
  # select(). This is because it implements `select_n`.
  pred, on_false, on_true = core.auto_insert_reshard(
      pred, on_false, on_true)
  return select_n_p.bind(pred, on_false, on_true)


def select(
    condlist: Sequence[ArrayLike],
    choicelist: Sequence[ArrayLike],
    default: ArrayLike = 0,
) -> Array:
  """Select values based on a series of conditions.

  JAX implementation of :func:`numpy.select`, implemented in terms
  of :func:`jax.lax.select_n`

  Args:
    condlist: sequence of array-like conditions. All entries must be mutually
      broadcast-compatible.
    choicelist: sequence of array-like values to choose. Must have the same length
      as ``condlist``, and all entries must be broadcast-compatible with entries
      of ``condlist``.
    default: value to return when every condition is False (default: 0).

  Returns:
    Array of selected values from ``choicelist`` corresponding to the first
    ``True`` entry in ``condlist`` at each location.

  See also:
    - :func:`jax.numpy.where`: select between two values based on a single condition.
    - :func:`jax.lax.select_n`: select between *N* values based on an index.

  Examples:
    >>> condlist = [
    ...    jnp.array([False, True, False, False]),
    ...    jnp.array([True, False, False, False]),
    ...    jnp.array([False, True, True, False]),
    ... ]
    >>> choicelist = [
    ...    jnp.array([1, 2, 3, 4]),
    ...    jnp.array([10, 20, 30, 40]),
    ...    jnp.array([100, 200, 300, 400]),
    ... ]
    >>> jnp.select(condlist, choicelist, default=0)
    Array([ 10,   2, 300,   0], dtype=int32)

    This is logically equivalent to the following nested ``where`` statement:

    >>> default = 0
    >>> jnp.where(condlist[0],
    ...   choicelist[0],
    ...   jnp.where(condlist[1],
    ...     choicelist[1],
    ...     jnp.where(condlist[2],
    ...       choicelist[2],
    ...       default)))
    Array([ 10,   2, 300,   0], dtype=int32)

    However, for efficiency it is implemented in terms of :func:`jax.lax.select_n`.
  """
  if len(condlist) != len(choicelist):
    msg = "condlist must have length equal to choicelist ({} vs {})"
    raise ValueError(msg.format(len(condlist), len(choicelist)))
  if len(condlist) == 0:
    raise ValueError("condlist must be non-empty")

  util.check_arraylike("select", *condlist, *choicelist, default)
  condlist = [asarray(cond) for cond in condlist]
  choicelist = [asarray(choice) for choice in choicelist]
  default = asarray(default)

  # Put the default at front with condition False because
  # argmax returns zero for an array of False values.
  choicelist = util.promote_dtypes(default, *choicelist)
  conditions = stack(broadcast_arrays(False, *condlist))
  idx = argmax(conditions.astype(bool), axis=0)
  return lax.select_n(*broadcast_arrays(idx, *choicelist))

