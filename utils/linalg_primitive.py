
def linalg_primitive(result_dtype, accepted_dtypes, ranks, result_shape, name,
                     multiple_results=False, supports_batching=True,
                     require_same=True, sharding_rule=None):
  dtype_rule = partial(
      lax.naryop_dtype_rule, result_dtype, accepted_dtypes, name,
      require_same=require_same)
  shape_rule = partial(
      linalg_shape_rule, multiple_results, supports_batching, ranks,
      result_shape, name)
  if sharding_rule is None and supports_batching:
    sharding_rule = partial(
        linalg_sharding_rule, multiple_results, shape_rule, ranks, name)
  vma_rule = partial(linalg_vma_rule, multiple_results, shape_rule, name)
  prim = core.Primitive(name)
  prim.multiple_results = multiple_results
  prim.def_impl(partial(dispatch.apply_primitive, prim))
  if multiple_results:
    prim.def_abstract_eval(
        partial(lax_utils.standard_multi_result_abstract_eval, prim,
                shape_rule, dtype_rule, lax_utils._standard_weak_type_rule,
                sharding_rule, vma_rule, None))
  else:
    prim.def_abstract_eval(
      partial(lax_utils.standard_abstract_eval, prim, shape_rule, dtype_rule,
              lax_utils._standard_weak_type_rule, sharding_rule,
              partial(core.standard_vma_rule, name), None, None))
  if supports_batching:
    batching.primitive_batchers[prim] = partial(
        batching.expand_dims_batcher, prim)
  return prim

