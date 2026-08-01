
def compute_on(compute_type: str):
  if not isinstance(compute_type, str):
    raise TypeError("`compute_on`'s compute_type argument must be a string.")
  _check_valid(compute_type)

  with extend_compute_type(compute_type):
    yield

