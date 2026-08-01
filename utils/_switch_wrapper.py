
def _switch_wrapper(*args, variables, rngs, n_branches):
  # first n_branches arguments are branches.
  # then scope, index, and the rest are *operands
  branches = args[:n_branches]
  scope, index, *operands = args[n_branches:]
  return lift.switch(
    index, branches, scope, *operands, variables=variables, rngs=rngs
  )

