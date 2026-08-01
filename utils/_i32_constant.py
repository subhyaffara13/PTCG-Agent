
def _i32_constant(v: int) -> ir.Value:
  if v < jnp.iinfo(jnp.int32).min or v > jnp.iinfo(jnp.int32).max:
    raise ValueError(f"Integer constant out of range for i32: {v}")
  return arith_dialect.constant(ir.IntegerType.get_signless(32), v)


def _i32_constant(v: int) -> ir.Value:
  return arith_dialect.constant(ir.IntegerType.get_signless(32), v)

