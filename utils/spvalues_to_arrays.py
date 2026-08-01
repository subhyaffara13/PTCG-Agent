
def spvalues_to_arrays(
    spenv: SparsifyEnv,
    spvalues: Any,
    ) -> Any:
  """Convert a pytree of spvalues to an equivalent pytree of (sparse) arrays."""
  def spvalue_to_array(spvalue):
    if spvalue.is_bcoo():
      return BCOO((spenv.data(spvalue), spenv.indices(spvalue)),
                  shape=spvalue.shape, indices_sorted=spvalue.indices_sorted,
                  unique_indices=spvalue.unique_indices)
    elif spvalue.is_bcsr():
      return BCSR((spenv.data(spvalue), spenv.indices(spvalue), spenv.indptr(spvalue)),
                  shape=spvalue.shape, indices_sorted=spvalue.indices_sorted,
                  unique_indices=spvalue.unique_indices)
    else:
      return spenv.data(spvalue)
  return tree_map(spvalue_to_array, spvalues, is_leaf=_is_spvalue)

