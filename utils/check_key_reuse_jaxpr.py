
def check_key_reuse_jaxpr(jaxpr: core.Jaxpr) -> None:
  """Check the jaxpr for key reuse."""
  jaxpr_type_signature(jaxpr)

