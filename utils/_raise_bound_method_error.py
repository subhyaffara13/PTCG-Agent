
def _raise_bound_method_error(transform_name: str):
  """Raises a standardized error for bound method usage with NNX transforms.

  Args:
    transform_name: Name of the transform (e.g., 'grad', 'jit', 'remat').
  """
  raise ValueError(
    f"nnx.{transform_name} does not support bound methods. "
    f"Use the decorator form @nnx.{transform_name} or call "
    f"nnx.{transform_name}(MyClass.method)(instance, ...) with the unbound method."
  )

