
def _vjp_check_ct_avals(cts, primal_avals):
  # TODO(mattjj): improve this error  by flattening with keys in the first place
  for ct, aval in zip(cts, primal_avals):
    if isinstance(ct, ad.Zero): continue
    ct_aval = typeof(ct)
    ct_aval_expected = aval.to_ct_aval()
    if (not core.typecompat(ct_aval, ct_aval_expected) and
        not _temporary_dtype_exception(ct_aval, ct_aval_expected)):
      raise ValueError(
          "unexpected JAX type (e.g. shape/dtype) for argument to VJP function: "
          f"got {ct_aval.str_short()}, but expected {ct_aval_expected.str_short()} "
          "because the corresponding output of the differentiated function had JAX type "
          f"{aval.str_short()}")

