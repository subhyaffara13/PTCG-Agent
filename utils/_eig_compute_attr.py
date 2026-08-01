
def _eig_compute_attr(compute):
  return _enum_attr(
      lapack.eig.ComputationMode.kComputeEigenvectors if compute
      else lapack.eig.ComputationMode.kNoEigenvectors
  )

