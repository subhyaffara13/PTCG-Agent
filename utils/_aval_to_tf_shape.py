
def _aval_to_tf_shape(aval: core.ShapedArray) -> tuple[int | None, ...]:

  """Generate a TF shape, possibly containing None for polymorphic dimensions."""
  aval = _jax_physical_aval(aval)
  return tuple(map(lambda d: None if export.is_symbolic_dim(d) else d,
                   aval.shape))

