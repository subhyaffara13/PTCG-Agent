
def _pow_by_squaring(x, n):
  if n < 0:
    return _pow_by_squaring(1 / x, -n)
  elif n == 0:
    return 1
  elif n % 2 == 0:
    return _pow_by_squaring(x * x, n / 2)
  elif n % 2 == 1:
    return x * _pow_by_squaring(x * x, (n - 1) / 2)

