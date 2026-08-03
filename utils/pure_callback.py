from typing import Any, Callable

def pure_callback(
    callback: Callable[..., Any],
    result_shape_dtypes: Any,
    *args: Any,
    sharding: Sharding | None = None,
    vmap_method: str | None = None,
    **kwargs: Any,
):
  """Calls a pure Python callback. Works under :func:`jit`/:func:`~vmap`/etc.

  For more explanation, see `External Callbacks`_.

  ``pure_callback`` enables calling a Python function in JIT-ed JAX functions.
  The input ``callback`` will be passed JAX arrays placed on a local CPU, and
  it should also return JAX arrays on CPU.

  The callback is treated as functionally pure, meaning it has no side-effects
  and its output value depends only on its argument values. As a consequence, it
  is safe to be called multiple times (e.g. when transformed by :func:`~vmap` or
  :func:`~pmap`), or not to be called at all when e.g. the output of a
  `jit`-decorated function has no data dependence on its value. Pure callbacks
  may also be reordered if data-dependence allows.

  .. warning::

     In the context of JAX transformations, Python exceptions should be
     considered side-effects: this means that intentionally raising an error
     within a `pure_callback` breaks the API contract, and the behavior of
     the resulting program is undefined.

  When `vmap`-ed the behavior will depend on the value of the ``vmap_method``.

  * Calling :func:`~jax.vmap` on a callback without an explicit ``vmap_method``
    raises a ``NotImplementedError``.
  * ``vmap_method="sequential"`` uses :func:`~jax.lax.map` to loop over
    the batched arguments, calling ``callback`` once for each batch element.
  * ``vmap_method="sequential_unrolled"`` is like ``sequential``, but the loop
    is unrolled.
  * ``vmap_method="expand_dims"`` calls ``callback`` with new axes of size ``1``
    added as the leading dimension unbatched inputs.
  * ``vmap_method="broadcast_all"`` behaves like ``expand_dims``, but the
    inputs are tiled to the expected batched shape.



  The current default behavior is to use ``vmap_method="sequential"`` when
  not specified, but this behavior is deprecated, and in the future, the
  default will be to raise a ``NotImplementedError`` unless ``vmap_method`` is
  explicitly specified.

  Args:
    callback: function to execute on the host. The callback is assumed to be a pure
      function (i.e. one without side-effects): if an impure function is passed, it
      may behave in unexpected ways, particularly under transformation. The callable
      will be passed PyTrees of arrays as arguments, and should return a PyTree of
      arrays that matches ``result_shape_dtypes``.
    result_shape_dtypes: pytree whose leaves have ``shape`` and ``dtype`` attributes,
      whose structure matches the expected output of the callback function at runtime.
      :class:`jax.ShapeDtypeStruct` is often used to define leaf values.
    *args: arguments to be passed to the callback function
    sharding: optional sharding that specifies the device from which the callback should
      be invoked.
    vmap_method: string specifying how the callback transforms under
      :func:`~jax.vmap` as described above.
    **kwargs: keyword arguments to be passed to the callback function

  Returns:
    result: a pytree of :class:`jax.Array` objects whose structure matches that of
      ``result_shape_dtypes``.

  See Also:
    - :func:`jax.experimental.io_callback`: callback designed for impure functions.
    - :func:`jax.debug.callback`: callback designed for general-purpose debugging.
    - :func:`jax.debug.print`: callback designed for printing.

  Examples:
    The behavior of ``pure_callback`` under :func:`~jax.vmap` is controlled by
    the ``vmap_method`` argument as described above. It is useful to consider
    some explicit examples that demonstrate the semantics. For example,
    consider the following function:

    >>> def callback(x, y):
    ...   print(jnp.shape(x), jnp.shape(y))
    ...   return x + y

    >>> def fun(x, y, *, vmap_method):
    ...   shape = jnp.broadcast_shapes(jnp.shape(x), jnp.shape(y))
    ...   dtype = jnp.result_type(x, y)
    ...   out_type = jax.ShapeDtypeStruct(shape, dtype)
    ...   return jax.pure_callback(callback, out_type, x, y,
    ...                            vmap_method=vmap_method)

    Calling this with ``vmap_method="expand_dims"`` adds a new axis of size ``1``
    to ``y``:

    >>> from functools import partial
    >>> x = jnp.arange(4)
    >>> y = 1.0
    >>> jax.vmap(partial(fun, vmap_method="expand_dims"), in_axes=(0, None))(x, y)
    (4,) (1,)
    Array([1., 2., 3., 4.], dtype=float32)

    Whereas, ``vmap_method="broadcast_all"`` adds an axis of size ``4`` to
    ``y``:

    >>> jax.vmap(partial(fun, vmap_method="broadcast_all"),
    ...          in_axes=(0, None))(x, y)
    (4,) (4,)
    Array([1., 2., 3., 4.], dtype=float32)

  .. _External Callbacks: https://docs.jax.dev/en/latest/external-callbacks.html
  """

  allowed_vmap_methods = ["sequential", "sequential_unrolled", "expand_dims",
                          "broadcast_all", "legacy_vectorized", None]
  if vmap_method not in allowed_vmap_methods:
    raise ValueError(
        f"vmap_method must be on of the allowed methods {allowed_vmap_methods}, "
        f"but got: {vmap_method}")

  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  tree_util.tree_map(_check_shape_dtype, result_shape_dtypes)
  result_avals = tree_util.tree_map(
      lambda x: core.ShapedArray(x.shape, x.dtype), result_shape_dtypes)
  flat_result_avals, out_tree = tree_util.tree_flatten(result_avals)
  out_flat = pure_callback_p.bind(
      *flat_args,
      callback=_FlatCallback(callback, in_tree),
      result_avals=tuple(flat_result_avals),
      sharding=sharding,
      vmap_method=vmap_method,
  )
  return tree_util.tree_unflatten(out_tree, out_flat)

