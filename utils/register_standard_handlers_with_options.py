
def register_standard_handlers_with_options(**kwargs):
  """Re-registers a select set of handlers with the given options.

  This is intended to override options en masse for the standard numeric
  TypeHandlers and their corresponding types (scalars, numpy arrays and
  jax.Arrays).

  Args:
    **kwargs: keyword arguments to pass to each of the standard handlers.
  """
  # TODO(b/314258967): clean those up.
  del kwargs['use_ocdbt'], kwargs['ts_context']
  GLOBAL_TYPE_HANDLER_REGISTRY.add(
      int, type_handlers.ScalarHandler(**kwargs), override=True
  )
  GLOBAL_TYPE_HANDLER_REGISTRY.add(
      float, type_handlers.ScalarHandler(**kwargs), override=True
  )
  GLOBAL_TYPE_HANDLER_REGISTRY.add(
      bytes, type_handlers.ScalarHandler(**kwargs), override=True
  )
  GLOBAL_TYPE_HANDLER_REGISTRY.add(
      np.number, type_handlers.ScalarHandler(**kwargs), override=True
  )
  GLOBAL_TYPE_HANDLER_REGISTRY.add(
      np.ndarray, type_handlers.NumpyHandler(**kwargs), override=True
  )
  GLOBAL_TYPE_HANDLER_REGISTRY.add(
      jax.Array, type_handlers.ArrayHandler(**kwargs), override=True
  )

