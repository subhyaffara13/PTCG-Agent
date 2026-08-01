
def _poch_z_derivative(z, m):
  """
  Defined in :
  https://functions.wolfram.com/GammaBetaErf/Pochhammer/20/01/01/
  """

  return (digamma(z + m) - digamma(z)) * poch(z, m)

