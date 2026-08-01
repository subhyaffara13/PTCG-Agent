
def standard_abstract_eval(
    prim, shape_rule, dtype_rule, weak_type_rule, sharding_rule, vma_rule,
    ur_rule, memory_space_rule, *avals, **kwargs):
  assert not prim.multiple_results
  for a in avals:
    if isinstance(a, state.AbstractRef):
      raise ValueError(f'Attempting to pass a Ref {a} to a primitive: '
                       f'{prim} -- did you forget to unpack ([...]) the ref?')
    if not isinstance(a, core.ShapedArray):
      raise ValueError(f'Attempting to pass an unexpected type {a} to a '
                       f'primitive: {prim}')
  weak_type = weak_type_rule(*avals, **kwargs)
  least_specialized = type(max(avals, key=_get_array_abstraction_level))
  if least_specialized is core.ShapedArray:
    core.check_avals_context_mesh(avals, prim.name)
    out_shape, out_dtype, out_sharding = call_shape_dtype_sharding_rule(
        prim, shape_rule, dtype_rule, sharding_rule, ur_rule, False,
        *avals, **kwargs)
    out_mat = manual_rule(prim, vma_rule, ur_rule, False, *avals, **kwargs)
    out_mem_space = (_default_memory_space_rule(prim, *avals, **kwargs)
                     if memory_space_rule is None else
                     memory_space_rule(*avals, **kwargs))
    out_aval = core.ShapedArray(
        out_shape, out_dtype, weak_type=weak_type, sharding=out_sharding,
        manual_axis_type=out_mat, memory_space=out_mem_space)
    core.check_avals_context_mesh([out_aval], prim.name)
    return out_aval
  else:
    raise TypeError(avals, least_specialized)

