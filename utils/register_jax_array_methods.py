
def register_jax_array_methods():
  """Call this function once to register methods of JAX arrays"""
  _set_shaped_array_attributes(core.ShapedArray)

  _set_array_base_attributes(ArrayImpl, exclude={'__getitem__'})
  _set_tracer_aval_forwarding(core.Tracer, exclude={*_impl_only_array_methods, "at"})
  _set_array_attributes(ArrayImpl)

  _set_array_abstract_methods(Array)

