
def assert_collection_of_arrays(inputs: Sequence[pytypes.Array]):
  """Checks if ``inputs`` is a collection of arrays."""
  if not isinstance(inputs, collections.abc.Collection):
    raise ValueError(f"`inputs` is not a collection of arrays: {inputs}.")

