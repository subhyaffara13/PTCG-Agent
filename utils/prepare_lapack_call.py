
def prepare_lapack_call(fn_base, dtype):
  """Initializes the LAPACK library and returns the LAPACK target name."""
  _lapack.initialize()
  return build_lapack_fn_target(fn_base, dtype)

