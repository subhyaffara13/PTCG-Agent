
def remat_transpose(out_cts, *args, jaxpr, prevent_cse, **params):
  # TODO(mattjj): avoid round-tripping into UndefinedPrimals
  args_ = [ad.UndefinedPrimal(x.aval) if isinstance(x, ad.GradAccum) else x
           for x in args]

  assert not jaxpr.constvars
  in_linear = [ad.is_undefined_primal(x) for x in args_]
  out_zeros = [type(ct) is ad_util.Zero for ct in out_cts]
  transposed_jaxpr_, in_zeros = transpose_jaxpr(
      pe.close_jaxpr(jaxpr), in_linear, out_zeros)
  transposed_jaxpr, consts = transposed_jaxpr_.jaxpr, transposed_jaxpr_.consts
  transposed_jaxpr = pe.convert_constvars_jaxpr(transposed_jaxpr)
  flat_args, _ = tree_flatten((args_, out_cts))
  if isinstance(prevent_cse, tuple):
    prevent_cse_, _ = partition_list(in_linear, prevent_cse)
    prevent_cse = tuple(prevent_cse_) + (True,) * (len(out_zeros) - sum(out_zeros))
  in_cts_nz = remat_p.bind(*consts, *flat_args, jaxpr=transposed_jaxpr,
                           prevent_cse=prevent_cse, **params)
  in_cts_nz_, in_zeros_ = iter(in_cts_nz), iter(in_zeros)
  for x in args:
    if isinstance(x, ad.GradAccum) and not next(in_zeros_):
      x.accum(next(in_cts_nz_))

