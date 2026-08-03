from typing import Callable

def _inout_vma_error(f: Callable, mesh: Mesh | AbstractMesh, tree: PyTreeDef,
                     specs: Specs, fails: list[core.ManualAxisType | NoFail]
                     ) -> str:
  fun_name = getattr(f, '__name__', str(f))
  msgs = []
  for (spec_key, spec), (fail_key, mat) in _iter_paths(tree, specs, fails):
    unmentioned = _unmentioned(mesh, spec)
    if len(unmentioned) > 1:
      need_vma = ','.join(map(str, order_wrt_mesh(mesh, _spec_to_vma(spec))))
      got_vma = ','.join(map(str, order_wrt_mesh(mesh, mat.varying)))
      diff = ','.join(map(str, order_wrt_mesh(
          mesh, [n for n in unmentioned if n in mat.varying])))
      msgs.append(
          f"* out_specs{keystr(spec_key)} is {spec} which implies that the "
          f"corresponding output value is only varying across mesh axes "
          f"{{{need_vma}}} and not {{{diff}}}, but it was inferred to be "
          f"possibly varying over {{{got_vma}}}")
    else:
      need_rep_, = unmentioned
      msgs.append(
          f"* out_specs{keystr(spec_key)} is {spec} which implies that the "
          f"corresponding output value is replicated across mesh axis "
          f"'{need_rep_}', but could not infer replication over any axes")
  assert msgs
  if len(msgs) == 1: msgs = [msgs[0][2:]]  # remove the bullet point
  msg = (f"shard_map applied to the function '{fun_name}' was given "
         f"out_specs which require replication which can't be statically "
         f"inferred given the mesh:\n\n"
         f"The mesh given has shape {tuple(mesh.shape.values())} with "
         f"corresponding axis names {mesh.axis_names}.\n\n"
         + '\n\n'.join(msgs) + '\n\n' +
         "Check if these output values are meant to be replicated over those "
         "mesh axes. If not, consider revising the corresponding out_specs "
         "entries. If so, consider disabling the check by passing the "
         "check_vma=False argument to `jax.shard_map`.")
  return msg

