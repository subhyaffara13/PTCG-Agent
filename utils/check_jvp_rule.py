
def check_jvp_rule(primals, _, *, err_tree, debug):
  # Check primals, discard tangents.
  check_p.bind(*primals, err_tree=err_tree, debug=debug)
  return [], []

