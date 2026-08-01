
def _transform_semaphore(ref_value, transforms, ref_aval):
  """Helper function for indexing into a semaphore during state_discharge."""
  if ref_value.shape == ref_aval.shape:
    return state_discharge.transform_array(ref_value, transforms)
  elif len(ref_value.shape) == 0:
    return ref_value
  else:
    raise ValueError(
        f"Semaphore value shape {ref_value.shape} does not match aval shape"
        f" {ref_aval.shape}"
    )

