
def check_shapes_equal(a: jax.typing.ArrayLike, b: jax.typing.ArrayLike):
  """Check that `a` and `b` have the same shape."""
  a_shape = a.shape if hasattr(a, 'shape') else np.asarray(a).shape
  b_shape = b.shape if hasattr(b, 'shape') else np.asarray(b).shape
  if a_shape != b_shape:
    raise ValueError(f'Shape mismatch: got {a_shape} and {b_shape}.')

