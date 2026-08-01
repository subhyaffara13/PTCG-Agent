
def _remat_bind(*args, jaxpr, prevent_cse, differentiated, policy):
  assert isinstance(prevent_cse, bool) or len(prevent_cse) == len(args)
  return core.Primitive.bind(remat_p, *args, jaxpr=jaxpr, prevent_cse=prevent_cse,
                             differentiated=differentiated, policy=policy)

