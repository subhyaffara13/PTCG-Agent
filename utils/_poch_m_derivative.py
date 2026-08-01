
def _poch_m_derivative(z, m):
  """
  Defined in :
  https://functions.wolfram.com/GammaBetaErf/Pochhammer/20/01/02/
  """

  return digamma(z + m) * poch(z, m)

