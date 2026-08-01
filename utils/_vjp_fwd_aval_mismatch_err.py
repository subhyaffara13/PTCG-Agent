
def _vjp_fwd_aval_mismatch_err(path, primal_aval, fwd_val):
  if not core.typematch(ty := typeof(fwd_val), primal_aval):
    raise TypeError(f"at {keystr(path)}, got fwd output type {ty.str_short()} "
                    f"which doesn't match primal output type {primal_aval.str_short()}")

