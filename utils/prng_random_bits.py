
def prng_random_bits(output: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return PRNGRandomBitsOp(output=output, loc=loc, ip=ip).result


def prng_random_bits(shape):
  return prng_random_bits_p.bind(shape=shape)

