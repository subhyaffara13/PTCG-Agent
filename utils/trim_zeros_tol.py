
def trim_zeros_tol(filt, tol, trim='fb'):
  filt = core.concrete_or_error(asarray, filt,
    "Error arose in the `filt` argument of trim_zeros_tol()")
  nz = (ufuncs.abs(filt) < tol)
  if reductions.all(nz):
    return array_creation.empty(0, _dtype(filt))
  start = argmin(nz) if 'f' in trim.lower() else 0
  end = argmin(nz[::-1]) if 'b' in trim.lower() else 0
  return filt[start:len(filt) - end]

