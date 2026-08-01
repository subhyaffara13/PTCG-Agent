
def naryop(result_dtype, accepted_dtypes, name, allow_extended_dtype=False,
           require_same_dtypes=True, ur_rule=None):
  dtype_rule = partial(naryop_dtype_rule, result_dtype, accepted_dtypes, name,
                       allow_extended_dtype=allow_extended_dtype,
                       require_same=require_same_dtypes)
  shape_rule = partial(broadcasting_shape_rule, name)
  sharding_rule = partial(broadcasting_sharding_rule, name)
  prim = standard_primitive(
      shape_rule, dtype_rule, name, sharding_rule=sharding_rule,
      vma_rule=partial(core.standard_vma_rule, name),
      ur_rule=partial(nary_ur_rule, name) if ur_rule is None else ur_rule)
  batching.defbroadcasting(prim)
  return prim

