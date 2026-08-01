
def _hyp1f1_x_derivative(a, b, x):
  """
  Define it as a serie using :
  https://functions.wolfram.com/HypergeometricFunctions/Hypergeometric1F1/20/01/04/
  """

  return a / b * hyp1f1(a + 1, b + 1, x)

