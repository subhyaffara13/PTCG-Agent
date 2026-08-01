
def io_callback(
    callback: Callable[..., Any],
    result_shape_dtypes: Any,
    *args: Any,
    sharding: Sharding | None = None,
    ordered: bool = False,
    **kwargs: Any,
):
  """Calls an impure Python callback.

  For more explanation, see `External Callbacks`_.

  Args:
    callback: function to execute on the host. It is assumed to be an impure function.
      If ``callback`` is pure, using :func:`jax.pure_callback` instead may lead to
      more efficient execution.
    result_shape_dtypes: pytree whose leaves have ``shape`` and ``dtype`` attributes,
      whose structure matches the expected output of the callback function at runtime.
      :class:`jax.ShapeDtypeStruct` is often used to define leaf values.
    *args: arguments to be passed to the callback function
    sharding: optional sharding that specifies the device from which the callback should
      be invoked.
    ordered: boolean specifying whether sequential calls to callback must be ordered.
    **kwargs: keyword arguments to be passed to the callback function

  Returns:
    result: a pytree of :class:`jax.Array` objects whose structure matches that of
      ``result_shape_dtypes``.

  See Also:
    - :func:`jax.pure_callback`: callback designed for pure functions.
    - :func:`jax.debug.callback`: callback designed for general-purpose debugging.
    - :func:`jax.debug.print`: callback designed for printing.

  .. _External Callbacks: https://docs.jax.dev/en/latest/notebooks/external_callbacks.html
  """
  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  tree_util.tree_map(_check_shape_dtype, result_shape_dtypes)
  flat_shape_dtypes, out_tree = tree_util.tree_flatten(result_shape_dtypes)
  flat_result_avals = map(lambda x: core.ShapedArray(x.shape, x.dtype),
                          flat_shape_dtypes)
  out_flat = io_callback_p.bind(
      *flat_args,
      callback=_FlatCallback(callback, in_tree),
      result_avals=tuple(flat_result_avals),
      sharding=sharding,
      ordered=ordered,
  )
  return tree_util.tree_unflatten(out_tree, out_flat)

