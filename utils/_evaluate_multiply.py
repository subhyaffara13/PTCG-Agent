
def _evaluate_multiply(v1, v2):
  try:
    if op.index(v1) == 1:
      return v2
  except:
    pass
  try:
    if op.index(v2) == 1:
      return v1
  except:
    pass
  return v1 * v2

