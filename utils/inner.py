
def inner(mode, pred, true_fn, false_fn, operands):
    return trace_cond(mode, cond_op, pred, true_fn, false_fn, operands)


def inner(proxy_mode, body_fn, args, kwargs, hints):
    if proxy_mode.enable_tracing:
        return trace_hints_wrapper(
            proxy_mode, hints_wrapper, body_fn, args, kwargs, hints
        )
    else:
        return hints_wrapper(body_fn, args, kwargs, hints)


def inner(mode, callable, operands):
    return trace_strict_mode(mode, strict_mode_op, callable, operands)


def inner(mode, *args, **kwargs):
    proxy_args = pytree.tree_map(mode.tracer.unwrap_proxy, args)
    proxy_kwargs = pytree.tree_map(mode.tracer.unwrap_proxy, kwargs)

    out_proxy = mode.tracer.create_proxy(
        "call_function",
        call_torchbind,
        proxy_args,
        proxy_kwargs,
    )
    out = call_torchbind(*args, **kwargs)

    obj, method, *_rest_args = args
    if isinstance(obj, torch.ScriptObject):
        ns, class_name = _ns_and_class_name(
            obj._type().qualified_name()  # type: ignore[attr-defined]
        )
        log.warning(
            "Tracing torchbind method %s.%s with real ScriptObject. This may"
            " cause the original object being mutated. If this is not intended,"
            ' You can register a fake class with torch._library.register_fake_class("%s::%s").',
            class_name,
            method,
            ns,
            class_name,
        )

    ret = track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)
    if "val" not in out_proxy.node.meta:
        if out is not None and not isinstance(out, (int, float, bool)):
            raise AssertionError(
                f"Currently, only these constant dtypes are supported to be returned from torchbind methods, got {type(out)}"
            )
        out_proxy.node.meta["val"] = out
    return ret


def inner(a: ArrayLike, b: ArrayLike, /):
    dtype = _dtypes_impl.result_type_impl(a, b)
    is_half = dtype == torch.float16 and (a.is_cpu or b.is_cpu)
    is_bool = dtype == torch.bool

    if is_half:
        # work around torch's "addmm_impl_cpu_" not implemented for 'Half'"
        dtype = torch.float32
    elif is_bool:
        dtype = torch.uint8

    a = _util.cast_if_needed(a, dtype)
    b = _util.cast_if_needed(b, dtype)

    result = torch.inner(a, b)

    if is_half:
        result = result.to(torch.float16)
    elif is_bool:
        result = result.to(torch.bool)
    return result


def inner(a, b):
    """
    Returns the inner product of a and b for arrays of floating point types.

    Like the generic NumPy equivalent the product sum is over the last dimension
    of a and b. The first argument is not conjugated.

    """
    fa = filled(a, 0)
    fb = filled(b, 0)
    if fa.ndim == 0:
        fa = fa.reshape((1,))
    if fb.ndim == 0:
        fb = fb.reshape((1,))
    return np.inner(fa, fb).view(MaskedArray)


def inner(a, b, /):
    """
    inner(a, b, /)

    Inner product of two arrays.

    Ordinary inner product of vectors for 1-D arrays (without complex
    conjugation), in higher dimensions a sum product over the last axes.

    Parameters
    ----------
    a, b : array_like
        If `a` and `b` are nonscalar, their last dimensions must match.

    Returns
    -------
    out : ndarray
        If `a` and `b` are both
        scalars or both 1-D arrays then a scalar is returned; otherwise
        an array is returned.
        ``out.shape = (*a.shape[:-1], *b.shape[:-1])``

    Raises
    ------
    ValueError
        If both `a` and `b` are nonscalar and their last dimensions have
        different sizes.

    See Also
    --------
    tensordot : Sum products over arbitrary axes.
    dot : Generalised matrix product, using second last dimension of `b`.
    vecdot : Vector dot product of two arrays.
    einsum : Einstein summation convention.

    Notes
    -----
    For vectors (1-D arrays) it computes the ordinary inner-product::

        np.inner(a, b) = sum(a[:]*b[:])

    More generally, if ``ndim(a) = r > 0`` and ``ndim(b) = s > 0``::

        np.inner(a, b) = np.tensordot(a, b, axes=(-1,-1))

    or explicitly::

        np.inner(a, b)[i0,...,ir-2,j0,...,js-2]
             = sum(a[i0,...,ir-2,:]*b[j0,...,js-2,:])

    In addition `a` or `b` may be scalars, in which case::

       np.inner(a,b) = a*b

    Examples
    --------
    Ordinary inner product for vectors:

    >>> import numpy as np
    >>> a = np.array([1,2,3])
    >>> b = np.array([0,1,0])
    >>> np.inner(a, b)
    2

    Some multidimensional examples:

    >>> a = np.arange(24).reshape((2,3,4))
    >>> b = np.arange(4)
    >>> c = np.inner(a, b)
    >>> c.shape
    (2, 3)
    >>> c
    array([[ 14,  38,  62],
           [ 86, 110, 134]])

    >>> a = np.arange(2).reshape((1,1,2))
    >>> b = np.arange(6).reshape((3,2))
    >>> c = np.inner(a, b)
    >>> c.shape
    (1, 1, 3)
    >>> c
    array([[[1, 3, 5]]])

    An example where `b` is a scalar:

    >>> np.inner(np.eye(2), 7)
    array([[7., 0.],
           [0., 7.]])

    """
    return (a, b)


def inner(
    a: ArrayLike, b: ArrayLike, *, precision: lax.PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
) -> Array:
  """Compute the inner product of two arrays.

  JAX implementation of :func:`numpy.inner`.

  Unlike :func:`jax.numpy.matmul` or :func:`jax.numpy.dot`, this always performs
  a contraction along the last dimension of each input.

  Args:
    a: array of shape ``(..., N)``
    b: array of shape ``(..., N)``
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array of shape ``(*a.shape[:-1], *b.shape[:-1])`` containing the batched vector
    product of the inputs.

  See also:
    - :func:`jax.numpy.vecdot`: conjugate multiplication along a specified axis.
    - :func:`jax.numpy.tensordot`: general tensor multiplication.
    - :func:`jax.numpy.matmul`: general batched matrix & vector multiplication.

  Examples:
    For 1D inputs, this implements standard (non-conjugate) vector multiplication:

    >>> a = jnp.array([1j, 3j, 4j])
    >>> b = jnp.array([4., 2., 5.])
    >>> jnp.inner(a, b)
    Array(0.+30.j, dtype=complex64)

    For multi-dimensional inputs, batch dimensions are stacked rather than broadcast:

    >>> a = jnp.ones((2, 3))
    >>> b = jnp.ones((5, 3))
    >>> jnp.inner(a, b).shape
    (2, 5)
  """
  a, b = util.ensure_arraylike("inner", a, b)
  if np.ndim(a) == 0 or np.ndim(b) == 0:
    if preferred_element_type is not None:
      a = a.astype(preferred_element_type)
      b = b.astype(preferred_element_type)
    return a * b
  return tensordot(a, b, (-1, -1), precision=precision,
                   preferred_element_type=preferred_element_type)

