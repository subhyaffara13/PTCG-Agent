
def prime_decomposition(n: int) -> list[int]:
  """Returns the prime decomposition of the given number `n` as a list of ints.

  A factor appears as many times in the list as the power up to which it divides
  `n`.
  """
  # This implementation should be sufficiently efficient for small `n`, which
  # should always be the case for us.
  prime_factors = []
  divisor = 2
  while divisor * divisor <= n:
    while n % divisor == 0:
      n //= divisor
      prime_factors.append(divisor)
    divisor += 1
  if n != 1:
    prime_factors.append(n)
  return prime_factors

