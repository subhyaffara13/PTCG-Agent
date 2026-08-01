
def _masked_array_error(xs, shardings, layouts, copy_semantics):
  raise ValueError("numpy masked arrays are not supported as direct inputs to JAX functions. "
                   "Use arr.filled() to convert the value to a standard numpy array.")

