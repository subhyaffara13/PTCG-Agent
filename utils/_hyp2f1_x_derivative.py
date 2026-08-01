
def _hyp2f1_x_derivative(a, b, c, x):
  """
  Define the derivative with regard to ``x`` :
  https://functions.wolfram.com/HypergeometricFunctions/Hypergeometric2F1/20/01/05/
  """

  return a * b / c * hyp2f1(a + 1, b + 1, c + 1, x)

