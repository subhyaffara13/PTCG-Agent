
def fallback_linearize_rule(_prim: core.Primitive,
                            _is_vjp, _nonzeros: Sequence[bool], *primals, **params):
  jvp = primitive_jvps.get(_prim)
  if not jvp:
    msg = f"Differentiation rule for '{_prim}' not implemented"
    raise NotImplementedError(msg)
  debug_jvp = debug_info("linearize_prim_jvp", jvp, primals, params)
  return linearize_from_jvp(lu.wrap_init(jvp, debug_info=debug_jvp),
                            _prim.multiple_results, _nonzeros, False, False,
                            primals, params)

