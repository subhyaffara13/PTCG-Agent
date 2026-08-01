
def stage(x: ArrayLike, /) -> Array:
  """Lifts a value into a trace.

  This operation is logically the identity function that lifts a value, such
  as a Python scalar or numpy ndarray, into the active trace. If we are outside
  any active trace contexts, stage returns a JAX array.
  """
  return stage_p.bind(x)

