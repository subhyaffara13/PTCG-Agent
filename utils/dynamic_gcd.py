
def dynamic_gcd(a: int, b: ir.Value) -> int:
  if a <= 0:
    raise ValueError("a must be strictly positive")
  if isinstance(b.type, ir.VectorType):
    # We don't actually know the values of the vector elements, so we pick 1
    # as the only safe value.
    return 1
  if not isinstance(b.type, ir.IntegerType) and not isinstance(
      b.type, ir.IndexType
  ):
    raise ValueError(f"Expected an integer dynamic value, got a {b.type}")
  if isinstance(b.owner, arith.ConstantOp):
    assert isinstance(b.owner.literal_value, int)
    return math.gcd(a, b.owner.literal_value)
  running_gcd = 1
  for factor in prime_decomposition(a):
    if utils.is_known_divisible(b, running_gcd * factor):
      running_gcd *= factor
  return running_gcd

