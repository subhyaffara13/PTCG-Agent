
def _mpmd_map_typecheck_rule(
    ctx_factory, *in_atoms, **params
):
  del ctx_factory  # Unused.
  return _mpmd_map_abstract_eval(
      *(x.aval for x in in_atoms), **params
  )

