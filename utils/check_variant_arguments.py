
def check_variant_arguments(variant_fn):
  """Raises `ValueError` if `variant_fn` got an unknown argument."""

  @functools.wraps(variant_fn)
  def wrapper(*args, **kwargs):
    unknown_args = set(kwargs.keys()) - _valid_kwargs_keys
    if unknown_args:
      raise ValueError(f"Unknown arguments in `self.variant`: {unknown_args}.")
    return variant_fn(*args, **kwargs)

  return wrapper

