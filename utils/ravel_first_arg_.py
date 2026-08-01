
def ravel_first_arg_(f, unravel, y_flat, *args):
  y = unravel(y_flat)
  ans = f(y, *args)
  ans_flat, _ = ravel_pytree(ans)
  return ans_flat

