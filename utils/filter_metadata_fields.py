
def filter_metadata_fields(
    pytree: PyTree, include_fields: Sequence[str]
) -> PyTree:
  """Returns a PyTree of dicts with keys in `include_fields`."""

  def _include(metadata):
    result = {}
    for f in include_fields:
      if hasattr(metadata, f):
        result[f] = getattr(metadata, f)
    return result

  return jax.tree.map(_include, pytree)

