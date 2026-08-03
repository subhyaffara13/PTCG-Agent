import functools

def _with_pmap(fn,
               broadcast_args_to_devices=True,
               reduce_fn="first_device_output",
               n_devices=None,
               axis_name="i",
               devices=None,
               in_axes=0,
               static_broadcasted_argnums=(),
               static_argnums=(),
               backend=None,
               **unused_kwargs):
  """Variant that applies `jax.pmap` to fn.

  Args:
    fn: A function to wrap.
    broadcast_args_to_devices: Whether to broadcast `fn` args to pmap format
      (i.e. pmapped axes' sizes == a number of devices).
    reduce_fn: A function to apply to outputs of `fn`.
    n_devices: A number of devices to use (can specify a `backend` if required).
    axis_name: An argument for `pmap`.
    devices: An argument for `pmap`.
    in_axes: An argument for `pmap`.
    static_broadcasted_argnums: An argument for `pmap`.
    static_argnums: An alias of ``static_broadcasted_argnums``.
    backend: An argument for `pmap`.
    **unused_kwargs: Unused kwargs (e.g. related to other variants).

  Returns:
    Wrapped `fn` that accepts `args` and `kwargs` and returns a superposition of
    `reduce_fn` and `fn` applied to them.

  Raises:
    ValueError: If `broadcast_args_to_devices` used with `in_axes` or
      `static_broadcasted_argnums`; if number of available devices is less than
      required; if pmappable arg axes' sizes are not equal to the number of
      devices.
    SkipTest: If the flag ``chex_skip_pmap_variant_if_single_device`` is set and
      there is only one device available.
  """
  if (FLAGS["chex_skip_pmap_variant_if_single_device"].value and
      jax.device_count() < 2):
    raise unittest.SkipTest(f"Only 1 device is available ({jax.devices()}).")

  if broadcast_args_to_devices and in_axes != 0:
    raise ValueError(
        "Do not use `broadcast_args_to_devices` when specifying `in_axes`.")

  # Set up a reduce function.
  if reduce_fn == "first_device_output":

    def reduce_fn(x):  # pylint: disable=function-redefined
      def _reduce_leaf(leaf):
        if (
            hasattr(leaf, "__getitem__")
            and hasattr(leaf, "shape")
            and leaf.shape
        ):
          if (
              not isinstance(leaf, jax.core.Tracer)
              and hasattr(leaf, "addressable_shards")
              and leaf.addressable_shards
          ):
            data = leaf.addressable_shards[0].data
            return data if not data.shape[0] else data[0]

          # Fallback for tracers or other indexable outputs.
          return leaf if not leaf.shape[0] else leaf[0]
        return leaf

      return tree_map(_reduce_leaf, x)

  elif reduce_fn == "identity" or reduce_fn is None:  # Identity.
    reduce_fn = lambda t: t

  if not static_argnums and static_argnums != 0:
    static_argnums = static_broadcasted_argnums
  if isinstance(static_argnums, int):
    static_argnums = (static_argnums,)

  pmap_kwargs = dict(
      axis_name=axis_name,
      devices=devices,
      in_axes=in_axes,
      static_broadcasted_argnums=static_argnums,
      backend=backend)
  pmapped_fn = jax.pmap(fn, **pmap_kwargs)

  @functools.wraps(pmapped_fn)
  def wrapper(*args: pytypes.ArrayTree, **kwargs: pytypes.ArrayTree):
    if kwargs and (in_axes != 0 or static_argnums):
      raise ValueError("Do not use kwargs with `in_axes` or `static_argnums` "
                       "in pmapped function.")
    devices_ = list(devices or jax.devices(backend))
    n_devices_ = n_devices or len(devices_)
    devices_ = devices_[:n_devices_]
    if len(devices_) != n_devices_:
      raise ValueError("Number of available devices is less than required for "
                       f"test ({len(devices_)} < {n_devices_})")

    def bcast_fn(x):
      x = jnp.asarray(x)
      x = jnp.broadcast_to(x, (n_devices_,) + x.shape)
      if not isinstance(x, jax.core.Tracer):
        mesh = jax.sharding.Mesh(np.array(devices_), ("_device_put_sharded",))
        sharding = jax.NamedSharding(mesh, jax.P("_device_put_sharded"))
        return jax.device_put(jnp.stack(list(x)), sharding)
      return x

    if broadcast_args_to_devices:
      args = [
          tree_map(bcast_fn, arg) if idx not in static_argnums else arg
          for idx, arg in enumerate(args)
      ]
      kwargs = tree_map(bcast_fn, kwargs)
    else:
      # Pmappable axes size must be equal to number of devices.
      in_axes_ = in_axes if isinstance(in_axes,
                                       (tuple, list)) else [in_axes] * len(args)
      is_pmappable_arg = [
          idx not in static_argnums and in_axes_[idx] is not None
          for idx in range(len(args))
      ]
      for is_pmappable_arg, arg in zip(is_pmappable_arg, args):
        if not is_pmappable_arg:
          continue
        if not all(
            x.shape[0] == n_devices_ for x in jax.tree_util.tree_leaves(arg)):
          shapes = tree_map(jnp.shape, arg)
          raise ValueError(
              f"Pmappable arg axes size must be equal to number of devices, "
              f"got: {shapes} (expected the first dim to be {n_devices_}). "
              "Consider setting `broadcast_args_to_devices=True`.")

    new_kwargs = dict(
        axis_name=axis_name,
        devices=devices_,
        in_axes=in_axes,
        static_broadcasted_argnums=static_argnums,
        backend=backend)

    # Re-compile fn if kwargs changed.
    nonlocal pmap_kwargs
    nonlocal pmapped_fn
    if new_kwargs != pmap_kwargs:
      pmap_kwargs = new_kwargs
      pmapped_fn = jax.pmap(fn, **pmap_kwargs)

    res = pmapped_fn(*args, **kwargs)
    return reduce_fn(res)

  return wrapper

