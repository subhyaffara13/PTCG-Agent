
def _make_output_specs_and_push_result_fun(
    info: FunctionInfo,
    specialization: Specialization,
    uid: int,
) -> Callable[..., Any]:
  """Creates a function that computes output specs and pushes the result to the result store."""
  assert specialization.in_specs_treedef is not None
  assert specialization.in_specs_leaves is not None
  assert specialization.out_specs_treedef is None
  assert specialization.out_specs_leaves is None
  assert specialization.devices is not None

  devices = specialization.devices

  def lowered_fun(*args, **kwargs) -> jax.Array:
    result = info.fun(*args, **kwargs)
    result_leaves, out_treedef = tree_util.tree_flatten(result)
    out_spec_leaves = tuple(_get_spec(x) for x in result_leaves)
    func_backend.SINGLETON_RESULT_STORE.push(uid, result_leaves)
    return _serialize_specs(out_treedef, out_spec_leaves, devices)

  out_specs_leaves, out_specs_treedef = tree_util.tree_flatten(
      _make_specs_for_serialized_specs(specialization.devices),
  )
  name = getattr(info.fun, "__name__", "unknown")
  name = f"{name}_output_specs_and_push_result"
  return _compile_to_executable(
      name=name,
      fun=lowered_fun,
      in_specs_treedef=specialization.in_specs_treedef,
      in_specs_leaves=specialization.in_specs_leaves,
      out_specs_treedef=out_specs_treedef,
      out_specs_leaves=tuple(out_specs_leaves),
      devices=specialization.devices,
  )

