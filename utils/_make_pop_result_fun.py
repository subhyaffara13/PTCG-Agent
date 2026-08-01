
def _make_pop_result_fun(
    info: FunctionInfo,
    specialization: Specialization,
    uid: int,
) -> Callable[..., Any]:
  """Makes a function that pops results from the result store."""
  assert specialization.out_specs_treedef is not None
  assert specialization.out_specs_leaves is not None
  assert specialization.devices is not None

  out_specs_treedef = specialization.out_specs_treedef

  def lowered_fun():
    result_leaves = func_backend.SINGLETON_RESULT_STORE.pop(uid)
    return tree_util.tree_unflatten(out_specs_treedef, result_leaves)

  in_specs_leaves, in_specs_treedef = tree_util.tree_flatten((
      # args
      (),
      # kwargs
      {},
  ))
  name = getattr(info.fun, "__name__", "unknown")
  name = f"{name}_pop_result"
  return _compile_to_executable(
      name=name,
      fun=lowered_fun,
      in_specs_treedef=in_specs_treedef,
      in_specs_leaves=tuple(in_specs_leaves),
      out_specs_treedef=specialization.out_specs_treedef,
      out_specs_leaves=specialization.out_specs_leaves,
      devices=specialization.devices,
  )

