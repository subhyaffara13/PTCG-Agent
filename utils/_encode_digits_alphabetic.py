
def _encode_digits_alphabetic(n: int) -> str:
  if n == -1:
    return '*'
  s = ''
  while len(s) == 0 or n:
    n, i = n // 26, n % 26
    s = chr(97 + i % 26) + s
  return s

