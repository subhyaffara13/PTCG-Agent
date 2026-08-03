from typing import Any, Callable

def repeat(x, repeats):
    old_size = list(x.get_size())
    if len(repeats) > len(old_size):
        old_size = [sympy.S.One] * (len(repeats) - len(old_size)) + old_size
        x = view(x, list(old_size))
    assert len(repeats) == len(x.get_size())

    new_size = list(x.get_size())

    zero_tensor = False
    for i in range(len(repeats)):
        if repeats[i] == 0:
            zero_tensor = True
        new_size[i] = new_size[i] * repeats[i]

    if zero_tensor:
        return empty(new_size, dtype=x.get_dtype(), device=x.get_device())
    if all((a == 1 or b == 1) for a, b in zip(repeats, old_size)):
        return clone(expand(x, new_size))

    x_loader: Callable[[Any], Any]

    def inner_fn(index):
        assert len(index) == len(repeats)
        index = list(index)
        for i in range(len(repeats)):
            if repeats[i] != 1:
                if old_size[i] == 1:
                    index[i] = sympy.S.Zero
                else:
                    index[i] = ModularIndexing(index[i], 1, old_size[i])
        return x_loader(index)

    # TODO Laith is there better check
    if not free_unbacked_symbols(old_size) and not free_unbacked_symbols(new_size):
        old_size_product = V.graph.sizevars.guarding_hint_or_throw(
            sympy_product(old_size)
        )
        if old_size_product > 0:
            # maybe realize the input but skip for unbacked symints since it'll
            # choke on the size hint.
            x.mark_reuse(
                V.graph.sizevars.guarding_hint_or_throw(sympy_product(new_size))
                // old_size_product
            )

    x_loader = x.make_loader()
    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=inner_fn,
        ranges=list(new_size),
    )


def repeat(a: ArrayLike, repeats: ArrayLikeOrScalar, axis=None):
    return torch.repeat_interleave(a, repeats, axis)


def repeat(a: Tensor, *repeat_shape) -> Tensor:
    repeat_shape = utils.extract_shape_from_varargs(repeat_shape, validate=False)
    torch._check(
        len(repeat_shape) >= len(a.shape),
        lambda: "repeat: Number of dimensions of repeat dims can not be smaller than number of dimensions of tensor",
    )

    if len(repeat_shape) == 0:
        return torch.clone(a)

    num_new_dimensions = len(repeat_shape) - a.ndim
    padded_shape = [1] * num_new_dimensions
    for dim_size in a.shape:
        padded_shape.append(dim_size)

    target_shape = tuple(
        padded_size * repeat_size
        for padded_size, repeat_size in zip(padded_shape, repeat_shape)
    )

    # return an empty tensor if one of the repeat_shape dimensions is zero
    if 0 in repeat_shape:
        return torch.empty(
            target_shape,
            dtype=a.dtype,
            device=a.device,
            requires_grad=a.requires_grad,
            memory_format=utils.suggest_memory_format(a),
        )

    urtensor_shape = target_shape
    urtensor_stride = utils.make_contiguous_strides_for(target_shape)
    for dim, dim_size in enumerate(padded_shape):
        # repeat each dimension by using unfold_copy operation
        urtensor_shape, urtensor_stride = _get_unfold_shape_stride(
            urtensor_shape, urtensor_stride, dim, dim_size, max(dim_size, 1)
        )

    # derive permute order by sorting urtensor strides
    enumerated_stride = list(enumerate(urtensor_stride))
    enumerated_stride.sort(key=operator.itemgetter(1), reverse=True)
    permute_order, _sorted_stride = zip(*enumerated_stride)

    # add new and expand dimensions according to urtensor
    repeat_xtensor = a.expand(urtensor_shape)

    # clone tensor to concretize expanded dimensions
    cloned_result = torch.clone(repeat_xtensor)

    # transpose axis so strides are in sorted order
    permuted_result = cloned_result.permute(permute_order)

    # reshape to get contiguous tensor with correct target shape
    return permuted_result.reshape(target_shape)


def repeat(item: T, count: int) -> Iterator[T]:
    for _ in range(count):
        yield item


def repeat(g: jit_utils.GraphContext, self, repeats):
    if not symbolic_helper._is_value(repeats):
        repeats = g.op("Constant", value_t=torch.LongTensor(repeats))
    if symbolic_helper._is_packed_list(repeats):
        repeat_size_len = len(symbolic_helper._unpack_list(repeats))
    else:
        const_repeats = symbolic_helper._maybe_get_const(repeats, "is")
        repeat_size_len = len(const_repeats)
    if self.isCompleteTensor():
        sizes = self.type().sizes()
        diff_dims = repeat_size_len - len(sizes)
        if diff_dims > 0:
            self = opset9.view(
                g, self, g.op("Constant", value_t=torch.tensor([1] * diff_dims + sizes))
            )
    return g.op("Tile", self, repeats)


def repeat(g: jit_utils.GraphContext, self, repeats):
    dtype = _type_utils.JitScalarType.INT64
    shape_ = ones_like(g, repeats, dtype)
    self = g.op("Expand", self, shape_)
    return g.op("Tile", self, repeats)


def repeat(x: Array, repeats: int | Array, /, *, axis: int | None = None) -> Array:
    if isinstance(repeats, torch.Tensor) and repeats.dtype in (torch.int8, torch.int16):
        # torch rejects short integers for the `repeat` argument:
        # https://github.com/pytorch/pytorch/issues/151311
        repeats = repeats.to(torch.int32)
    return torch.repeat_interleave(x, repeats, axis)


def repeat(a, repeats, axis=None):
    """
    Repeat each element of an array after themselves

    Parameters
    ----------
    a : array_like
        Input array.
    repeats : int or array of ints
        The number of repetitions for each element.  `repeats` is broadcasted
        to fit the shape of the given axis.
    axis : int, optional
        The axis along which to repeat values.  By default, use the
        flattened input array, and return a flat output array.

    Returns
    -------
    repeated_array : ndarray
        Output array which has the same shape as `a`, except along
        the given axis.

    See Also
    --------
    tile : Tile an array.
    unique : Find the unique elements of an array.

    Examples
    --------
    >>> import numpy as np
    >>> np.repeat(3, 4)
    array([3, 3, 3, 3])
    >>> x = np.array([[1,2],[3,4]])
    >>> np.repeat(x, 2)
    array([1, 1, 2, 2, 3, 3, 4, 4])
    >>> np.repeat(x, 3, axis=1)
    array([[1, 1, 1, 2, 2, 2],
           [3, 3, 3, 4, 4, 4]])
    >>> np.repeat(x, [1, 2], axis=0)
    array([[1, 2],
           [3, 4],
           [3, 4]])

    """
    return _wrapfunc(a, 'repeat', repeats, axis=axis)


def repeat(what, times=10):
    '''Getting types from annotations.

    :param what: what to repeat.
    :param -t, --times: how many times to repeat.'''

    return what * times


def repeat(output: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], dimension: _Union[int, _ods_ir.IntegerAttr], times: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return RepeatOp(output=output, source=source, dimension=dimension, times=times, loc=loc, ip=ip).result


def repeat(a: ArrayLike, repeats: ArrayLike, axis: int | None = None, *,
           total_repeat_length: int | None = None,
           out_sharding: NamedSharding | P | None = None) -> Array:
  """Construct an array from repeated elements.

  JAX implementation of :func:`numpy.repeat`.

  Args:
    a: N-dimensional array
    repeats: 1D integer array specifying the number of repeats. Must match the
      length of the repeated axis.
    axis: integer specifying the axis of ``a`` along which to construct the
      repeated array. If None (default) then ``a`` is first flattened.
    total_repeat_length: this must be specified statically for ``jnp.repeat``
      to be compatible with :func:`~jax.jit` and other JAX transformations.
      If ``sum(repeats)`` is larger than the specified ``total_repeat_length``,
      the remaining values will be discarded. If ``sum(repeats)`` is smaller
      than ``total_repeat_length``, the final value will be repeated.

  Returns:
    an array constructed from repeated values of ``a``.

  See Also:
    - :func:`jax.numpy.tile`: repeat a full array rather than individual values.

  Examples:
    Repeat each value twice along the last axis:

    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.repeat(a, 2, axis=-1)
    Array([[1, 1, 2, 2],
           [3, 3, 4, 4]], dtype=int32)

    If ``axis`` is not specified, the input array will be flattened:

    >>> jnp.repeat(a, 2)
    Array([1, 1, 2, 2, 3, 3, 4, 4], dtype=int32)

    Pass an array to ``repeats`` to repeat each value a different number of times:

    >>> repeats = jnp.array([2, 3])
    >>> jnp.repeat(a, repeats, axis=1)
    Array([[1, 1, 2, 2, 2],
           [3, 3, 4, 4, 4]], dtype=int32)

    In order to use ``repeat`` within ``jit`` and other JAX transformations, the
    size of the output must be specified statically using ``total_repeat_length``:

    >>> jit_repeat = jax.jit(jnp.repeat, static_argnames=['axis', 'total_repeat_length'])
    >>> jit_repeat(a, repeats, axis=1, total_repeat_length=5)
    Array([[1, 1, 2, 2, 2],
           [3, 3, 4, 4, 4]], dtype=int32)

    If `total_repeat_length` is smaller than ``sum(repeats)``, the result will be truncated:

    >>> jit_repeat(a, repeats, axis=1, total_repeat_length=4)
    Array([[1, 1, 2, 2],
           [3, 3, 4, 4]], dtype=int32)

    If it is larger, then the additional entries will be filled with the final value:

    >>> jit_repeat(a, repeats, axis=1, total_repeat_length=7)
    Array([[1, 1, 2, 2, 2, 2, 2],
           [3, 3, 4, 4, 4, 4, 4]], dtype=int32)
  """
  if core.is_dim(repeats):
    util.check_arraylike("repeat", a)
  else:
    util.check_arraylike("repeat", a, repeats)
  a = asarray(a)

  if axis is None:
    a = a.ravel()
    axis = 0

  if out_sharding is not None:
    return _auto_repeat(_repeat, a, repeats, axis, total_repeat_length,
                        out_sharding)
  ctx_mesh = get_abstract_mesh()
  if ctx_mesh._any_axis_explicit:
    aval = core.typeof(a)
    if axis is None or aval.sharding.spec[axis] is not None:
      raise ValueError(
          "Please pass sharding to `jnp.repeat` via `out_sharding` parameter.")
    assert axis is not None and aval.sharding.spec[axis] is None
    out_sharding = (NamedSharding(ctx_mesh, P())
                    if aval.sharding.mesh.empty else aval.sharding)
    return _auto_repeat(_repeat, a, repeats, axis, total_repeat_length,
                        out_sharding)
  try:
    return _repeat(repeats, a, axis=axis,
                   total_repeat_length=total_repeat_length)
  except core.ShardingTypeError:
    raise ValueError(
        "Please pass sharding to `jnp.repeat` via `out_sharding` parameter.")


def repeat(x: jax.Array, repeats: int, axis: int) -> jax.Array:
  axis = util.canonicalize_axis(axis, x.ndim)
  reps = [repeats if i == axis else 1 for i in range(x.ndim)]
  return jnp.tile(x, reps)

