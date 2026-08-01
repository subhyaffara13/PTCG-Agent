
def _bcoo_sum_duplicates(data: Array, indices: Array, *, spinfo: SparseInfo, nse: int | None) -> tuple[Array, Array]:
  if nse is not None:
    nse = core.concrete_or_error(operator.index, nse, "nse argument of bcoo_sum_duplicates.")
  return bcoo_sum_duplicates_p.bind(data, indices, spinfo=spinfo, nse=nse)

