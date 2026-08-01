
def _register_numpy_and_scalar_handlers():
  """Registers the Numpy and Scalar handlers."""
  numpy_handler = get_pathways_numpy_handler()
  scalar_handler = get_pathways_scalar_handler()
  type_handler_registry.register_type_handler(
      int, scalar_handler, override=True
  )
  type_handler_registry.register_type_handler(
      float, scalar_handler, override=True
  )
  type_handler_registry.register_type_handler(
      bytes, scalar_handler, override=True
  )
  type_handler_registry.register_type_handler(
      np.number, scalar_handler, override=True
  )
  type_handler_registry.register_type_handler(
      np.ndarray, numpy_handler, override=True
  )

