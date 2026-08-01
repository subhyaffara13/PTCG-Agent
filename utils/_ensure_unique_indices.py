
def _ensure_unique_indices(spenv, spvalue):
  """Return an spvalue representation with deduplicated indices."""
  if spvalue.is_dense() or spvalue.unique_indices:
    return spvalue
  arr = spvalues_to_arrays(spenv, spvalue)
  arr = arr.sum_duplicates(nse=arr.nse, remove_zeros=False)
  return arrays_to_spvalues(spenv, arr)

