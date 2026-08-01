
def remat_impl(*args, jaxpr, prevent_cse, differentiated, policy):
  del prevent_cse, differentiated, policy  # Unused.
  return core.eval_jaxpr(jaxpr, (), *args)

