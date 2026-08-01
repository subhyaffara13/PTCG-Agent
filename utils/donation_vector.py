
def donation_vector(donate_argnums, donate_argnames, in_tree,
                    kws: bool = True) -> tuple[bool, ...]:
  """Returns a tuple with a boolean value for each leaf in args and kwargs.

  What if a user specifies donate_argnums but calls the function with kwargs
  or vice-versa? In that case, in `resolve_argnums` using the signature of the
  function, the counterpart (donate_argnames or donate_argnums respectively) is
  calculated so when this function is called both donate_argnums and
  donate_argnames are available. This allows JAX to donate kwargs when only
  donate_argnums is specified and vice-versa.

  When both donate_argnums and donate_argnames are specified, only the args and
  kwargs specified are donated.
  """
  res: list[bool] = []
  if kws:
    args_tree, kwargs_tree = treedef_children(in_tree)
  else:
    args_tree, kwargs_tree = in_tree, None
  for i, arg in enumerate(args_tree.children()):
    donate = bool(i in donate_argnums)
    res.extend((donate,) * arg.num_leaves)
  if kwargs_tree is not None:
    for key, val in zip(kwargs_tree.node_data()[1], kwargs_tree.children()):  # pyrefly: ignore[unsupported-operation]
      donate = key in donate_argnames
      res.extend((donate,) * val.num_leaves)
  return tuple(res)

