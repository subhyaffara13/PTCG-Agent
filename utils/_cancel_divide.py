
def _cancel_divide(num, denom):
  num = list(num)
  for a in denom:
    i = next((i for i, b in enumerate(num) if definitely_equal(a, b)), None)
    if i is None:
      break  # couldn't cancel
    del num[i]
  else:
    return math.prod(num)

