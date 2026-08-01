
def standard_primitive(shape_rule, dtype_rule, name,
                       weak_type_rule=None, sharding_rule=None, vma_rule=None,
                       ur_rule=None, memory_space_rule=None):
  weak_type_rule = weak_type_rule or _standard_weak_type_rule
  prim = core.Primitive(name)
  prim.def_impl(partial(dispatch.apply_primitive, prim))
  prim.def_abstract_eval(
      partial(standard_abstract_eval, prim, shape_rule, dtype_rule,
              weak_type_rule, sharding_rule, vma_rule, ur_rule,
              memory_space_rule))
  return prim

