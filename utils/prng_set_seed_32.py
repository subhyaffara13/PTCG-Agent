
def prng_set_seed_32(seeds: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PRNGSeed32Op:
  return PRNGSeed32Op(seeds=seeds, loc=loc, ip=ip)

