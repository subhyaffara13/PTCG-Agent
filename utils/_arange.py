
def _arange(start: ArrayLike | DimSize, stop: ArrayLike | DimSize | None = None,
            step: ArrayLike | None = None, dtype: DTypeLike | None = None,
            out_sharding: NamedSharding | None = None) -> Array:
  # Validate inputs
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "arange")
  util.check_arraylike_or_none("arange", start, stop, step)

  # Ensure start/stop/step are concrete
  start_name = "stop" if stop is None and step is None else "start"
  start = core.concrete_or_error(None, start, f"It arose in the jnp.arange argument '{start_name}'")
  stop = core.concrete_or_error(None, stop, "It arose in the jnp.arange argument 'stop'")
  step = core.concrete_or_error(None, step, "It arose in the jnp.arange argument 'step'")

  # Ensure start/stop/step are scalars
  for name, val in [(start_name, start), ("stop", stop), ("step", step)]:
    if val is not None and np.ndim(val) != 0:
      raise ValueError(f"jax.numpy.arange: arguments must be scalars; got {name}={val}")

  # Handle symbolic dimensions
  if any(core.is_symbolic_dim(v) for v in (start, stop, step)):
    if stop is None:
      start, stop = 0, start
    if step is None:
      step = 1
    return _arange_dynamic(start, stop, step, dtype or dtypes.default_int_dtype())

  if dtype is None:
    dtype = dtypes.result_type(start, *(x for x in [stop, step] if x is not None))
  dtype = dtypes.jax_dtype(dtype)

  if iscomplexobj(start) or iscomplexobj(stop) or iscomplexobj(step):
    raise ValueError(
        "Passing complex start/stop/step to jnp.arange is no longer supported"
        " starting in JAX v0.10.0.")

  if stop is None:
    start, stop = 0, start

  if step is not None:
    # arange(N, M, K)
    if (dtype is not None and
        dtypes.issubdtype(dtype, np.floating) and
        dtypes.finfo(dtype).bits < 32):
      working_dtype = np.dtype('float32')
    else:
      working_dtype = dtype
    size = max(0, int(np.ceil((stop - start) / step)))
    return lax.convert_element_type(
        lax.add(lax.convert_element_type(start, working_dtype),
                lax.mul(lax.convert_element_type(step, working_dtype),
                        lax.broadcasted_iota(working_dtype, (size,), 0,
                                             out_sharding=out_sharding))),
        dtype)
  elif start == 0:
    # arange(M) or arange(0, M)
    size = max(0, int(np.ceil(stop)))
    return lax.broadcasted_iota(dtype, (size,), 0, out_sharding=out_sharding)
  else:
    # arange(N, M)
    size = max(0, int(np.ceil(stop - start)))
    return lax.add(lax.convert_element_type(start, dtype),
                    lax.broadcasted_iota(dtype, (size,), 0, out_sharding=out_sharding))

