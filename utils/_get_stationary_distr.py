
def _get_stationary_distr(c):
  """Gets stationary distribution of transition matrix c."""

  eigenvals, left_eigenvecs, _ = la.eig(c, left=True, right=True)

  mask = abs(eigenvals - 1.) < 1e-10
  left_eigenvecs = left_eigenvecs[:, mask]
  num_stationary_eigenvecs = np.shape(left_eigenvecs)[1]
  if num_stationary_eigenvecs != 1:
    raise ValueError('Expected 1 stationary distribution, but found %d' %
                     num_stationary_eigenvecs)
  left_eigenvecs *= 1. / sum(left_eigenvecs)

  return left_eigenvecs.real.flatten()

