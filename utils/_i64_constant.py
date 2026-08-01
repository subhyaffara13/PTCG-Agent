
def _i64_constant(v: int) -> ir.Value:
  if v < jnp.iinfo(jnp.int64).min or v > jnp.iinfo(jnp.int64).max:
    raise ValueError(f"Integer constant out of range for i64: {v}")
  return arith_dialect.constant(ir.IntegerType.get_signless(64), v)


def _i64_constant(v: int) -> ir.Value:
  return arith_dialect.constant(ir.IntegerType.get_signless(64), v)

