
def ct_check(accum, ct):
  if config.disable_bwd_checks.value:
    return
  ct_aval = ct.aval if type(ct) is Zero else typeof(ct)
  if not core.typematch(ct_aval, accum.aval, no_dtype_check=True):
    raise ValueError(f"Expected cotangent type {accum.aval.str_short()} but "
                     f"got {ct_aval.str_short()}")

