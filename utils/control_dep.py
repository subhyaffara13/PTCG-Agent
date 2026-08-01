
def control_dep(src, dst):
  """Adds a control dependency from src to dst."""
  return jax.ffi.ffi_call("control_dep", (), has_side_effect=True)(src, dst)

