
def set_error_if(pred: Array, /, msg: str) -> None:
  """Set the internal error state if any element of `pred` is `True`.

  This function is used inside JAX computations to detect runtime errors without
  immediately halting execution. When this function is traced (e.g., inside
  :func:`jax.jit`), the corresponding error message and its traceback are
  recorded. At execution time, if `pred` contains any `True` values, the error
  state is set, but execution continues without interruption. The recorded error
  can later be raised using :func:`raise_if_error`.

  If the error state has already been set, subsequent errors are ignored and
  will not override the existing error.

  For multi-device environments, in explicit mode, users must call
  :func:`error_checking_context` to initialize a new error tracking state that
  matches the device mesh. In auto mode, implicit cross-device communication may
  occur inside this function, which could impact performance. A warning is
  issued in such cases.

  When exporting a function with `jax.export`, error checking must be explicitly
  wrapped using :func:`wrap_for_export` before export and
  :func:`unwrap_from_import` after import.

  Args:
    pred: A JAX boolean array. If any element of `pred` is `True`, the internal
      error state will be set.
    msg: The corresponding error message to be raised later.
  """
  # TODO(jakevdp): remove this import and express the following using lax APIs.
  import jax.numpy as jnp  # pyrefly: ignore[missing-import]

  if _error_storage.ref is None:
    with core.eval_context():
      _initialize_error_code_ref()
    assert _error_storage.ref is not None

  # Get the traceback.
  traceback = source_info_util.current().traceback
  assert traceback is not None
  traceback = traceback.as_python_traceback()
  assert isinstance(traceback, TracebackType)
  traceback = traceback_util.filter_traceback(traceback)
  assert isinstance(traceback, TracebackType)

  with _error_list_lock:
    new_error_code = np.uint32(len(_error_list))
    _error_list.append((msg, traceback))

  out_sharding = core.typeof(_error_storage.ref).sharding
  in_sharding: NamedSharding = core.typeof(pred).sharding

  # Reduce `pred`.
  if all(dim is None for dim in out_sharding.spec):  # single-device case.
    pred = pred.any()
  else:  # multi-device case.
    has_auto_axes = mesh_lib.AxisType.Auto in in_sharding.mesh.axis_types
    if has_auto_axes:  # auto mode.
      warnings.warn(
          "When at least one mesh axis of `pred` is in auto mode, calling"
          " `set_error_if` will cause implicit communication between devices."
          " To avoid this, consider converting the mesh axis in auto mode to"
          " explicit mode.",
          RuntimeWarning,
      )
      pred = pred.any()  # reduce to a single scalar
    else:  # explicit mode.
      if out_sharding.mesh != in_sharding.mesh:
        raise ValueError(
            "The error code state and the predicate must be on the same mesh, "
            f"but got {out_sharding.mesh} and {in_sharding.mesh} respectively. "
            "Please use `with error_checking_context()` to redefine the error "
            "code state based on the mesh."
        )
      pred = shard_map.shard_map(
          partial(jnp.any, keepdims=True),
          mesh=out_sharding.mesh,
          in_specs=in_sharding.spec,
          out_specs=out_sharding.spec,
      )(pred)  # perform per-device reduction

  error_code = _error_storage.ref[...]
  should_update = jnp.logical_and(error_code == jnp.uint32(_NO_ERROR), pred)
  error_code = jnp.where(should_update, new_error_code, error_code)
  # TODO(ayx): support vmap and shard_map.
  _error_storage.ref[...] = error_code

