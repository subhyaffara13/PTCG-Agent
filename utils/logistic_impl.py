
def logistic_impl(x, accuracy):
  del accuracy
  one = _const(x, 1)
  return div(one, add(one, exp(neg(x))))

