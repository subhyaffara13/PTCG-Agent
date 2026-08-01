
def _vjp_bwd_aval_mismatch_err(path, primal_aval, ct):
  if config.disable_bwd_checks.value:
    return
  if isinstance(ct, ad_util.Zero):
    return
  if isinstance(primal_aval, AbstractRef):
    primal_aval = primal_aval.inner_aval
  expected = primal_aval.to_ct_aval()
  ct_aval = ct.aval if isinstance(ct, ad_util.SymbolicZero) else typeof(ct)
  if (not core.typematch(expected, ct_aval) and
      not _temporary_dtype_exception(expected, ct_aval) and
      getattr(expected, 'dtype', None) is not dtypes.float0):
    result = f"at output{keystr(path)} " if path else ""
    raise ValueError(
        f"{result}the bwd rule produced an output of type {ct_aval.str_short()}"
        f" which doesn't match expected type {expected.str_short()}")

