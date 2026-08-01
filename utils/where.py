
def where(cond, a, b):
    def fn(*args):
        return ops.where(*args)

    if isinstance(a, (float, int)):
        a = constant_like(a)(b)
    if isinstance(b, (float, int)):
        b = constant_like(b)(a)

    args = [cond, a, b]
    dtype = get_promoted_dtype(
        args[1], args[2], type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )
    indices = [i for i, x in enumerate(args) if isinstance(x, TensorBox)]
    for i, x in zip(indices, broadcast_tensors(*[args[i] for i in indices])):
        args[i] = x
    for i in range(len(args)):
        if isinstance(args[i], ir.Constant):
            args[i] = ExpandView.create(args[i], list(args[indices[0]].get_size()))
    return make_pointwise(fn, override_return_dtype=dtype)(
        args[0], to_dtype(args[1], dtype), to_dtype(args[2], dtype)
    )


def where(
    condition: ArrayLike,
    x: ArrayLikeOrScalar | None = None,
    y: ArrayLikeOrScalar | None = None,
    /,
):
    if (x is None) != (y is None):
        raise ValueError("either both or neither of x and y should be given")

    if condition.dtype != torch.bool:
        condition = condition.to(torch.bool)

    if x is None and y is None:
        result = torch.where(condition)
    else:
        result = torch.where(condition, x, y)
    return result


def where(
    pred: Tensor,
    a: TensorOrNumberLikeType | None = None,
    b: TensorOrNumberLikeType | None = None,
):
    """ """

    if a is None or b is None:
        raise NotImplementedError

    utils.check_same_device(pred, a, b, allow_cpu_scalar_tensors=True)
    torch._check(
        pred.dtype is torch.bool,
        lambda: f"expected predicate to be bool, got {pred.dtype}",
    )

    pred, a, b = _maybe_broadcast(pred, a, b)
    return prims.where(pred, a, b)


def where(g: jit_utils.GraphContext, condition, self=None, other=None, _outputs=None):
    # Assumes that torch.where's first argument takes only Bool and Byte tensors.
    if not symbolic_helper._is_bool(condition):
        condition = g.op("Cast", condition, to_i=_C_onnx.TensorProtoDataType.BOOL)
    if self is None:
        condition = opset9.nonzero(g, condition)
        return symbolic_helper._unbind_helper(
            g, condition, g.op("Constant", value_t=torch.tensor(1)), _outputs
        )
    # pyrefly: ignore [bad-argument-type]
    return g.op("Where", condition, self, other)


def where(g: jit_utils.GraphContext, condition, self=None, other=None, _outputs=None):
    # Assumes that torch.where's first argument takes only Bool and Byte tensors.
    if not symbolic_helper._is_bool(condition):
        condition = g.op("Cast", condition, to_i=_C_onnx.TensorProtoDataType.BOOL)
    if self is None:
        condition = nonzero(g, condition)
        return symbolic_helper._unbind_helper(
            g, condition, g.op("Constant", value_t=torch.tensor(1)), _outputs
        )
    # pyrefly: ignore [bad-argument-type]
    return g.op("Where", condition, self, other)


def where(func, *args, **kwargs):
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=3, len_kwargs=0
    )
    if not torch.is_tensor(args[0]):
        raise ValueError(f"__torch_dispatch__, {func}: expected args[0] to be a tensor")
    mx = args[1]
    my = args[2]
    if not is_masked_tensor(mx):
        mx = MaskedTensor(mx, torch.ones_like(mx, dtype=torch.bool))
    if not is_masked_tensor(my):
        my = MaskedTensor(my, torch.ones_like(my, dtype=torch.bool))
    new_data = func(args[0], mx.get_data(), my.get_data())
    new_mask = func(args[0], mx.get_mask(), my.get_mask())
    return MaskedTensor(new_data, new_mask)


def where(condition, given_condition=None, **kwargs):
    """
    Returns the domain where a condition is True.

    Examples
    ========

    >>> from sympy.stats import where, Die, Normal
    >>> from sympy import And

    >>> D1, D2 = Die('a', 6), Die('b', 6)
    >>> a, b = D1.symbol, D2.symbol
    >>> X = Normal('x', 0, 1)

    >>> where(X**2<1)
    Domain: (-1 < x) & (x < 1)

    >>> where(X**2<1).set
    Interval.open(-1, 1)

    >>> where(And(D1<=D2, D2<3))
    Domain: (Eq(a, 1) & Eq(b, 1)) | (Eq(a, 1) & Eq(b, 2)) | (Eq(a, 2) & Eq(b, 2))
    """
    if given_condition is not None:  # If there is a condition
        # Recompute on new conditional expr
        return where(given(condition, given_condition, **kwargs), **kwargs)

    # Otherwise pass work off to the ProbabilitySpace
    return pspace(condition).where(condition, **kwargs)


def where(condition: Array, x1: Array | complex, x2: Array | complex, /) -> Array:
    x1, x2 = _fix_promotion(x1, x2)
    return torch.where(condition, x1, x2)


def where(cond, left_op, right_op, use_numexpr: bool = True):
    """
    Evaluate the where condition cond on left_op and right_op.

    Parameters
    ----------
    cond : np.ndarray[bool]
    left_op : return if cond is True
    right_op : return if cond is False
    use_numexpr : bool, default True
        Whether to try to use numexpr.
    """
    assert _where is not None
    if use_numexpr:
        return _where(cond, left_op, right_op)
    else:
        return _where_standard(cond, left_op, right_op)


def where(condition, x=_NoValue, y=_NoValue):
    """
    Return a masked array with elements from `x` or `y`, depending on condition.

    .. note::
        When only `condition` is provided, this function is identical to
        `nonzero`. The rest of this documentation covers only the case where
        all three arguments are provided.

    Parameters
    ----------
    condition : array_like, bool
        Where True, yield `x`, otherwise yield `y`.
    x, y : array_like, optional
        Values from which to choose. `x`, `y` and `condition` need to be
        broadcastable to some shape.

    Returns
    -------
    out : MaskedArray
        A masked array with `masked` elements where the condition is masked,
        elements from `x` where `condition` is True, and elements from `y`
        elsewhere.

    See Also
    --------
    numpy.where : Equivalent function in the top-level NumPy module.
    nonzero : The function that is called when x and y are omitted

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array(np.arange(9.).reshape(3, 3), mask=[[0, 1, 0],
    ...                                                    [1, 0, 1],
    ...                                                    [0, 1, 0]])
    >>> x
    masked_array(
      data=[[0.0, --, 2.0],
            [--, 4.0, --],
            [6.0, --, 8.0]],
      mask=[[False,  True, False],
            [ True, False,  True],
            [False,  True, False]],
      fill_value=1e+20)
    >>> np.ma.where(x > 5, x, -3.1416)
    masked_array(
      data=[[-3.1416, --, -3.1416],
            [--, -3.1416, --],
            [6.0, --, 8.0]],
      mask=[[False,  True, False],
            [ True, False,  True],
            [False,  True, False]],
      fill_value=1e+20)

    """

    # handle the single-argument case
    missing = (x is _NoValue, y is _NoValue).count(True)
    if missing == 1:
        raise ValueError("Must provide both 'x' and 'y' or neither.")
    if missing == 2:
        return nonzero(condition)

    # we only care if the condition is true - false or masked pick y
    cf = filled(condition, False)
    xd = getdata(x)
    yd = getdata(y)

    # we need the full arrays here for correct final dimensions
    cm = getmaskarray(condition)
    xm = getmaskarray(x)
    ym = getmaskarray(y)

    # deal with the fact that masked.dtype == float64, but we don't actually
    # want to treat it as that.
    if x is masked and y is not masked:
        xd = np.zeros((), dtype=yd.dtype)
        xm = np.ones((),  dtype=ym.dtype)
    elif y is masked and x is not masked:
        yd = np.zeros((), dtype=xd.dtype)
        ym = np.ones((),  dtype=xm.dtype)

    data = np.where(cf, xd, yd)
    mask = np.where(cf, xm, ym)
    mask = np.where(cm, np.ones((), dtype=mask.dtype), mask)

    # collapse the mask, for backwards compatibility
    mask = _shrink_mask(mask)

    return masked_array(data, mask=mask)


def where(condition, x=None, y=None, /):
    """
    where(condition, [x, y], /)

    Return elements chosen from `x` or `y` depending on `condition`.

    .. note::
        When only `condition` is provided, this function is a shorthand for
        ``np.asarray(condition).nonzero()``. Using `nonzero` directly should be
        preferred, as it behaves correctly for subclasses. The rest of this
        documentation covers only the case where all three arguments are
        provided.

    Parameters
    ----------
    condition : array_like, bool
        Where True, yield `x`, otherwise yield `y`.
    x, y : array_like
        Values from which to choose. `x`, `y` and `condition` need to be
        broadcastable to some shape.

    Returns
    -------
    out : ndarray
        An array with elements from `x` where `condition` is True, and elements
        from `y` elsewhere.

    See Also
    --------
    choose
    nonzero : The function that is called when x and y are omitted

    Notes
    -----
    If all the arrays are 1-D, `where` is equivalent to::

        [xv if c else yv
         for c, xv, yv in zip(condition, x, y)]

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(10)
    >>> a
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> np.where(a < 5, a, 10*a)
    array([ 0,  1,  2,  3,  4, 50, 60, 70, 80, 90])

    This can be used on multidimensional arrays too:

    >>> np.where([[True, False], [True, True]],
    ...          [[1, 2], [3, 4]],
    ...          [[9, 8], [7, 6]])
    array([[1, 8],
           [3, 4]])

    The shapes of x, y, and the condition are broadcast together:

    >>> x, y = np.ogrid[:3, :4]
    >>> np.where(x < y, x, 10 + y)  # both x and 10+y are broadcast
    array([[10,  0,  0,  0],
           [10, 11,  1,  1],
           [10, 11, 12,  2]])

    >>> a = np.array([[0, 1, 2],
    ...               [0, 2, 4],
    ...               [0, 3, 6]])
    >>> np.where(a < 4, a, -1)  # -1 is broadcast
    array([[ 0,  1,  2],
           [ 0,  2, -1],
           [ 0,  3, -1]])
    """
    return (condition, x, y)


def where(condition: ArrayLike, /, *, size: int | None = None,
          fill_value: None | ArrayLike | tuple[ArrayLike, ...] = None
          ) -> tuple[Array, ...]:
  ...


def where(condition: ArrayLike, x: ArrayLike, y: ArrayLike, /) -> Array:
  ...


def where(condition, x=None, y=None, /, *, size=None, fill_value=None):
  """Select elements from two arrays based on a condition.

  JAX implementation of :func:`numpy.where`.

  .. note::
     when only ``condition`` is provided, ``jnp.where(condition)`` is equivalent
     to ``jnp.nonzero(condition)``. For that case, refer to the documentation of
     :func:`jax.numpy.nonzero`. The docstring below focuses on the case where
     ``x`` and ``y`` are specified.

  The three-term version of ``jnp.where`` lowers to :func:`jax.lax.select`.

  Args:
    condition: boolean array. Must be broadcast-compatible with ``x`` and ``y`` when
      they are specified.
    x: arraylike. Should be broadcast-compatible with ``condition`` and ``y``, and
      typecast-compatible with ``y``.
    y: arraylike. Should be broadcast-compatible with ``condition`` and ``x``, and
      typecast-compatible with ``x``.
    size: integer, only referenced when ``x`` and ``y`` are ``None``. For details,
      see :func:`jax.numpy.nonzero`.
    fill_value: only referenced when ``x`` and ``y`` are ``None``. For details,
      see :func:`jax.numpy.nonzero`.

  Returns:
    An array of dtype ``jnp.result_type(x, y)`` with values drawn from ``x`` where ``condition``
    is True, and from ``y`` where condition is ``False``. If ``x`` and ``y`` are ``None``, the
    function behaves differently; see :func:`jax.numpy.nonzero` for a description of the return
    type.

  See Also:
    - :func:`jax.numpy.nonzero`
    - :func:`jax.numpy.argwhere`
    - :func:`jax.lax.select`

  Notes:
    Special care is needed when the ``x`` or ``y`` input to :func:`jax.numpy.where` could
    have a value of NaN. Specifically, when a gradient is taken with :func:`jax.grad`
    (reverse-mode differentiation), a NaN in either ``x`` or ``y`` will propagate into the
    gradient, regardless of the value of ``condition``.  More information on this behavior
    and workarounds is available in the `JAX FAQ
    <https://docs.jax.dev/en/latest/faq.html#gradients-contain-nan-where-using-where>`_.

  Examples:
    When ``x`` and ``y`` are not provided, ``where`` behaves equivalently to
    :func:`jax.numpy.nonzero`:

    >>> x = jnp.arange(10)
    >>> jnp.where(x > 4)
    (Array([5, 6, 7, 8, 9], dtype=int32),)
    >>> jnp.nonzero(x > 4)
    (Array([5, 6, 7, 8, 9], dtype=int32),)

    When ``x`` and ``y`` are provided, ``where`` selects between them based on
    the specified condition:

    >>> jnp.where(x > 4, x, 0)
    Array([0, 0, 0, 0, 0, 5, 6, 7, 8, 9], dtype=int32)
  """
  if x is None and y is None:
    util.check_arraylike("where", condition)
    return nonzero(condition, size=size, fill_value=fill_value)
  else:
    util.check_arraylike("where", condition, x, y)
    if size is not None or fill_value is not None:
      raise ValueError("size and fill_value arguments cannot be used in "
                       "three-term where function.")
    if x is None or y is None:
      raise ValueError("Either both or neither of the x and y arguments "
                       "should be provided to jax.numpy.where, got "
                       f"{x} and {y}.")
    return util._where(condition, x, y)

