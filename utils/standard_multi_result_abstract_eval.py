
def standard_multi_result_abstract_eval(
    prim, shape_rule, dtype_rule, weak_type_rule, sharding_rule, vma_rule,
    ur_rule, *avals, **kwargs):
  assert prim.multiple_results
  assert all(isinstance(aval, core.ShapedArray) for aval in avals), avals
  least_specialized = max(map(type, avals), key=_get_array_abstraction_level)
  weak_types = weak_type_rule(*avals, **kwargs)
  if least_specialized is core.ShapedArray:
    core.check_avals_context_mesh(avals, prim.name)
    out_shapes, out_dtypes, out_shardings = call_shape_dtype_sharding_rule(
        prim, shape_rule, dtype_rule, sharding_rule, ur_rule, True,
        *avals, **kwargs)
    out_mats = manual_rule(prim, vma_rule, ur_rule, True, *avals, **kwargs)
    out_mem_spaces = multi_mem_space_rule(prim, len(out_shapes), *avals, **kwargs)
    if isinstance(weak_types, bool):
      weak_types = (weak_types,) * len(out_shapes)
    out_avals = [core.ShapedArray(s, d, weak_type=weak_type, sharding=sh,
                                  manual_axis_type=mat, memory_space=ms)
                 for s, d, weak_type, sh, mat, ms in zip(
                     out_shapes, out_dtypes, weak_types, out_shardings,
                     out_mats, out_mem_spaces)]
    core.check_avals_context_mesh(out_avals, prim.name)
    return out_avals
  else:
    raise TypeError(avals, least_specialized)

