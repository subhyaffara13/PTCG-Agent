from typing import Callable

def assert_axis_dimension_comparator(tensor: Array, axis: int,
                                     pass_fn: Callable[[int], bool],
                                     error_string: str):
  """Asserts that `pass_fn(tensor.shape[axis])` passes.

  Used to implement ==, >, >=, <, <= checks.

  Args:
    tensor: A JAX array.
    axis: An integer specifying which axis to assert.
    pass_fn: A callable which takes the size of the give dimension and returns
      false when the assertion should fail.
    error_string: string which is inserted in assertion failure messages -
      'expected tensor to have dimension {error_string} on axis ...'.

  Raises:
    AssertionError: if `pass_fn(tensor.shape[axis], val)` does not return true.
  """
  if not isinstance(tensor, (jax.Array, np.ndarray)):
    tensor = np.asarray(tensor)  # np is broader than jnp (it supports strings)
  if axis >= len(tensor.shape) or axis < -len(tensor.shape):
    raise AssertionError(
        f"Expected tensor to have dim {error_string} on axis "
        f"'{axis}' but axis '{axis}' not available: tensor rank is "
        f"'{len(tensor.shape)}'.")
  if not pass_fn(tensor.shape[axis]):
    raise AssertionError(
        f"Expected tensor to have dimension {error_string} on axis"
        f" '{axis}' but got '{tensor.shape[axis]}' instead.")

