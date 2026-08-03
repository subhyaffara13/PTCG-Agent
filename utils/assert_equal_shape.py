from typing import Optional, Union

def assert_equal_shape(
    inputs: Sequence[Array],
    *,
    dims: Optional[Union[int, Sequence[int]]] = None) -> None:
  """Checks that all arrays have the same shape.

  Args:
    inputs: A collection of arrays.
    dims: An optional integer or sequence of integers. If not provided, every
      dimension of every shape must match. If provided, equality of shape will
      only be asserted for the specified dim(s), i.e. to ensure all of a group
      of arrays have the same size in the first two dimensions, call
      ``assert_equal_shape(tensors_list, dims=(0, 1))``.

  Raises:
    AssertionError: If the shapes of all arrays at specified dims do not match.
    ValueError: If the provided ``dims`` are invalid indices into any of arrays;
      or if ``inputs`` is not a collection of arrays.
  """
  _ai.assert_collection_of_arrays(inputs)

  # NB: Need explicit dims argument, closing over it triggers linter bug.
  def extract_relevant_dims(shape, dims):
    try:
      if dims is None:
        return shape
      elif isinstance(dims, int):
        return shape[dims]
      else:
        return [shape[d] for d in dims]
    except IndexError as err:
      raise ValueError(
          f"Indexing error when trying to extra dim(s) {dims} from array shape "
          f"{shape}") from err

  shape = extract_relevant_dims(inputs[0].shape, dims)
  expected_shapes = [shape] * len(inputs)
  shapes = [extract_relevant_dims(x.shape, dims) for x in inputs]
  if shapes != expected_shapes:
    if dims is not None:
      msg = f"Arrays have different shapes at dims {dims}: {shapes}"
    else:
      msg = f"Arrays have different shapes: {shapes}."
    raise AssertionError(msg)

