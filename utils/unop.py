
def unop(result_dtype, accepted_dtypes, name, supports_narrow_ints=True):
  dtype_rule = partial(unop_dtype_rule, result_dtype, accepted_dtypes, name,
                       supports_narrow_ints=supports_narrow_ints)
  prim = standard_primitive(_attrgetter('shape'), dtype_rule, name,
                            sharding_rule=_attrgetter('sharding'),
                            vma_rule=lambda x, **kwargs: x.mat.varying,
                            ur_rule=partial(unop_ur_rule, name))
  batching.defvectorized(prim)
  return prim

