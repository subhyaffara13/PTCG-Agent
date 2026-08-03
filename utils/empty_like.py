from typing import Any

def empty_like(
    prototype: ArrayLike,
    dtype: DTypeLike | None = None,
    order: NotImplementedType = "K",
    subok: NotImplementedType = False,
    shape=None,
):
    result = torch.empty_like(prototype, dtype=dtype)
    if shape is not None:
        result = result.reshape(shape)
    return result


def empty_like(
    a: TensorLikeType,
    *,
    dtype: torch.dtype | None = None,
    device: DeviceLikeType | None = None,
    layout: torch.layout | None = None,
    pin_memory: bool = False,
    requires_grad: bool = False,
    memory_format: torch.memory_format = torch.preserve_format,
) -> TensorLikeType:
    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    if memory_format != torch.preserve_format:
        return torch.empty(
            a.shape,
            dtype=dtype,
            layout=layout,
            device=device,
            requires_grad=requires_grad,
            pin_memory=pin_memory,
            memory_format=memory_format,
        )

    # memory_format == torch.preserve_format
    logical_to_physical_perm, _ = (
        utils.compute_elementwise_output_logical_to_physical_perm(a)
    )
    # identity perm is [2, 1, 0]
    return torch.empty_permuted(
        a.shape,
        logical_to_physical_perm,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
        requires_grad=requires_grad,
    )


def empty_like(
    g: jit_utils.GraphContext,
    input,
    dtype,
    layout,
    device,
    pin_memory=False,
    memory_format=None,
):
    return zeros_like(g, input, dtype, layout, device, pin_memory)


def empty_like(
    g: jit_utils.GraphContext,
    input,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=False,
    memory_format=None,
):
    return zeros_like(g, input, dtype, layout, device, pin_memory)


def empty_like(
    x: Array,
    /,
    xp: Namespace,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.empty_like(x, dtype=dtype, **kwargs)


def empty_like(
    prototype, dtype=None, order="K", subok=True, shape=None, *, device=None
):
    """
    empty_like(
        prototype,
        /,
        dtype=None,
        order='K',
        subok=True,
        shape=None,
        *,
        device=None,
    )
    --

    Return a new array with the same shape and type as a given array.

    Parameters
    ----------
    prototype : array_like
        The shape and data-type of `prototype` define these same attributes
        of the returned array.
    dtype : data-type, optional
        Overrides the data type of the result.
    order : {'C', 'F', 'A', or 'K'}, optional
        Overrides the memory layout of the result. 'C' means C-order,
        'F' means F-order, 'A' means 'F' if `prototype` is Fortran
        contiguous, 'C' otherwise. 'K' means match the layout of `prototype`
        as closely as possible.
    subok : bool, optional.
        If True, then the newly created array will use the sub-class
        type of `prototype`, otherwise it will be a base-class array. Defaults
        to True.
    shape : int or sequence of ints, optional.
        Overrides the shape of the result. If order='K' and the number of
        dimensions is unchanged, will try to keep order, otherwise,
        order='C' is implied.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    out : ndarray
        Array of uninitialized (arbitrary) data with the same
        shape and type as `prototype`.

    See Also
    --------
    ones_like : Return an array of ones with shape and type of input.
    zeros_like : Return an array of zeros with shape and type of input.
    full_like : Return a new array with shape of input filled with value.
    empty : Return a new uninitialized array.

    Notes
    -----
    Unlike other array creation functions (e.g. `zeros_like`, `ones_like`,
    `full_like`), `empty_like` does not initialize the values of the array,
    and may therefore be marginally faster. However, the values stored in the
    newly allocated array are arbitrary. For reproducible behavior, be sure
    to set each element of the array before reading.

    Examples
    --------
    >>> import numpy as np
    >>> a = ([1,2,3], [4,5,6])                         # a is array-like
    >>> np.empty_like(a)
    array([[-1073741821, -1073741821,           3],    # uninitialized
           [          0,           0, -1073741821]])
    >>> a = np.array([[1., 2., 3.],[4.,5.,6.]])
    >>> np.empty_like(a)
    array([[ -2.00000715e+000,   1.48219694e-323,  -2.00000572e+000], # uninitialized
           [  4.38791518e-305,  -2.00000715e+000,   4.17269252e-309]])

    """
    return (prototype,)


def empty_like(prototype: ArrayLike | DuckTypedArray,
               dtype: DTypeLike | None = None,
               shape: Any = None, *,
               device: xc.Device | Sharding | None = None) -> Array:
  """Create an empty array with the same shape and dtype as an array.

  JAX implementation of :func:`numpy.empty_like`. Because XLA cannot create
  an un-initialized array, :func:`jax.numpy.empty` will always return an
  array full of zeros.

  Args:
    a: Array-like object with ``shape`` and ``dtype`` attributes.
    shape: optionally override the shape of the created array.
    dtype: optionally override the dtype of the created array.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.empty`
    - :func:`jax.numpy.zeros_like`
    - :func:`jax.numpy.ones_like`
    - :func:`jax.numpy.full_like`

  Examples:
    >>> x = jnp.arange(4)
    >>> jnp.empty_like(x)  # doctest: +SKIP
    Array([0, 0, 0, 0], dtype=int32)
    >>> jnp.empty_like(x, dtype=bool)  # doctest: +SKIP
    Array([False, False, False, False], dtype=bool)
    >>> jnp.empty_like(x, shape=(2, 3))  # doctest: +SKIP
    Array([[0, 0, 0],
           [0, 0, 0]], dtype=int32)
  """
  if not (hasattr(prototype, 'dtype') and hasattr(prototype, 'shape')):  # support duck typing
    m = getattr(prototype, '__jax_array__', None)
    if m is not None:
      prototype = m()
    util.check_arraylike("ones_like", prototype)
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "ones_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  return lax.full_like(prototype, 0, dtype, shape,
                       sharding=util.canonicalize_device_to_sharding(device))


def empty_like(x: object):
  """Create an empty PyTree of possibly uninitialized values.

  Args:
    x: A PyTree with leaves specifying the shape and dtype of
      the uninitialized object.

  Returns:
    A PyTree with the same structure as ``x``, but with uninitialized
    values.

  See Also:
    :func:`jax.lax.empty`
  """
  return tree_util.tree_map(lambda leaf: empty(leaf.shape, leaf.dtype), x)

