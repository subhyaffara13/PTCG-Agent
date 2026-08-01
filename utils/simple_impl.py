
def simple_impl(prim):
  prim.def_impl(partial(apply_primitive, prim))

