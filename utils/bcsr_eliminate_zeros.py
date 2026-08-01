
def bcsr_eliminate_zeros(mat: BCSR, nse: int | None = None) -> BCSR:
  """Eliminate zeros in BCSR representation."""
  return BCSR.from_bcoo(bcoo.bcoo_eliminate_zeros(mat.to_bcoo(), nse=nse))

