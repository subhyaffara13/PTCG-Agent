import functools

def dyn_dot(x, y):
  assert len(x) == len(y)
  return functools.reduce(arith.addi, (arith.muli(a, b) for a, b in zip(x, y)))

