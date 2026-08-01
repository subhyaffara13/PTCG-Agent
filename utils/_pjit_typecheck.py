
def _pjit_typecheck(ctx_factory, *in_atoms, jaxpr, **params):
  return core._check_call(ctx_factory, jit_p, in_atoms,
                          dict(params, call_jaxpr=jaxpr.jaxpr))

