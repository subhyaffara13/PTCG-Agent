
def _evaluate_add(v1, v2):
  try:
    if op.index(v1) == 0:
      return v2
  except:
    pass
  try:
    if op.index(v2) == 0:
      return v1
  except:
    pass
  return v1 + v2

