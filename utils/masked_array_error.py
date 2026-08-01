
def masked_array_error(*args, **kwargs):
  raise ValueError(
      "numpy masked arrays are not supported as direct inputs to JAX functions."
      " Use arr.filled() to convert the value to a standard numpy array.")

