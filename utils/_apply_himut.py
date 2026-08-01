
def _apply_himut(final_qdds, hi_args, out_mut):
  out_mut_ = iter(out_mut)
  for i, a in enumerate(final_qdds):
    if isinstance(a, core.AvalQDD):
      lo_vals = it.islice(out_mut_, len(a.aval.lo_ty_qdd(a.qdd)))
      a.aval.update_from_loval(a.qdd, hi_args[i], *lo_vals)  # pyrefly: ignore[missing-attribute]
  assert next(out_mut_, None) is None

