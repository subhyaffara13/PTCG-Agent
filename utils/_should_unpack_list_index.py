
def _should_unpack_list_index(x):
  """Helper for eliminate_deprecated_list_indexing."""
  return (isinstance(x, (np.ndarray, Array))
          and np.ndim(x) != 0
          or isinstance(x, (Sequence, slice))
          or x is Ellipsis or x is None)

